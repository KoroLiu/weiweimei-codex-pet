"""Generate narration with the selected local IndexTTS profile and prepare video assets."""
import argparse
import hashlib
import json
import math
import re
import subprocess
import sys
from pathlib import Path

VIDEO = Path(__file__).resolve().parents[1]
TTS = Path(r"C:\IndexTTS")
sys.path.insert(0, str(TTS / "scripts"))
from audio_common import inspect_audio


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def voice_settings(profile):
    fields = ("id", "referenceSha256", "language", "durationFactor", "emotionVectorUI", "emotionWeight",
              "emotionRandom", "seed", "generationParameters", "intervalSilenceMs", "maxTextTokensPerSegment",
              "generationMode", "manualPauseInsertion", "sentencePauseMs")
    return {field: profile.get(field) for field in fields}


def sentence_segments(scene, profile):
    text = scene["say"].strip()
    if scene.get("keepGreetingTogether"):
        parts = [text]
    else:
        parts = [part.strip() for part in re.split(r"(?<=[。！？!?])", text) if part.strip()]
    if any(not part or len(part) > 40 for part in parts):
        raise ValueError(f"{scene['id']}: each complete sentence must be 1..40 characters in this workflow.")
    return [{"text": part, "durationFactor": profile["durationFactor"],
             "pauseAfterMs": profile["sentencePauseMs"] if index < len(parts) - 1 else 0}
            for index, part in enumerate(parts)]


def caption_cues(scene, sample, duration, start_frame, fps):
    segments = sample.get("segments")
    if segments and all("voiceSentence" in cue for cue in scene["cues"]):
        bounds = []
        cursor = start_frame / fps
        for segment in segments:
            end = cursor + segment["audio"]["duration_seconds"]
            bounds.append((cursor, end))
            cursor = end + segment["addedPauseAfterMs"] / 1000
        groups = [[cue for cue in scene["cues"] if cue["voiceSentence"] == index]
                  for index in range(len(bounds))]
        if not all(groups) or sum(map(len, groups)) != len(scene["cues"]):
            raise ValueError(f"{scene['id']}: caption voiceSentence indices do not match the spoken sentences.")
    else:
        bounds = [(start_frame / fps, start_frame / fps + duration)]
        groups = [scene["cues"]]
    result = []
    for (start, end), group in zip(bounds, groups):
        weights = [max(1, len(re.sub(r"[\s，。！？、,.!?→]+", "", cue["text"]))) for cue in group]
        cursor = 0
        for cue, weight in zip(group, weights):
            start_ms = (start + (end - start) * cursor / sum(weights)) * 1000
            cursor += weight
            end_ms = (start + (end - start) * cursor / sum(weights)) * 1000
            result.append({"text": cue["text"], "startMs": start_ms, "endMs": end_ms,
                           "timestampMs": None, "confidence": None, "pageBreakAfter": True})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-name", required=True)
    parser.add_argument("--scenes", nargs="+", help="Regenerate only these scenes; reuse the other current audio tracks.")
    parser.add_argument("--existing-plan", help="Prepare assets from a completed local batch without generating again.")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.batch_name):
        parser.error("Use an ASCII batch name with letters, numbers, hyphens or underscores.")
    if Path(sys.prefix).resolve() != Path(r"D:\Anaconda\envs\index-tts").resolve():
        raise RuntimeError("Run with the index-tts Conda environment.")
    all_scenes = read_json(VIDEO / "storyboard.json")
    scenes = all_scenes
    reused_timing = {}
    if args.scenes:
        requested = set(args.scenes)
        if requested - {scene["id"] for scene in all_scenes}:
            parser.error("An unknown scene ID was requested.")
        scenes = [scene for scene in all_scenes if scene["id"] in requested]
        reused_timing = {scene["id"]: scene for scene in read_json(VIDEO / "voiceover-timing.json")}
        for scene in all_scenes:
            if scene["id"] not in requested:
                current = reused_timing[scene["id"]]
                if len(current["audioTracks"]) != 1 or current["audioTracks"][0]["text"] != scene["say"]:
                    raise RuntimeError(f"{scene['id']} also changed; include it in --scenes.")
    profile_link = read_json(VIDEO / "voice-profile.json")
    profile = read_json(profile_link["profilePath"])
    settings = voice_settings(profile)
    if reused_timing:
        for scene in all_scenes:
            if scene["id"] not in set(args.scenes) and reused_timing[scene["id"]].get("voiceSettings") != settings:
                raise RuntimeError("Voice settings also changed; regenerate every scene without --scenes.")
    reference = Path(profile["reference"])
    if hashlib.sha256(reference.read_bytes()).hexdigest() != profile["referenceSha256"]:
        raise RuntimeError("The approved reference audio changed.")
    output = TTS / "outputs/weiweimei/pet-intro" / args.batch_name
    asset_dir = VIDEO / "public/voiceover" / args.batch_name
    if asset_dir.exists() or (output.exists() and not args.existing_plan):
        raise RuntimeError("Keep the previous audio; use a new batch name.")
    plans = VIDEO / "voiceover-plans"
    plans.mkdir(exist_ok=True)
    plan_path = plans / f"{args.batch_name}.json"
    samples = []
    for scene in scenes:
        text = scene["say"].strip()
        sentence_mode = profile.get("generationMode") == "complete_sentences"
        if not text or (not sentence_mode and len(text) > 40):
            raise ValueError(f"{scene['id']}: keep each scene at 1..40 characters for this whole-scene workflow.")
        sample = {"id": scene["id"], "label": scene["title"], "text": text,
                        "reference": str(reference), "referenceExcerptSeconds": profile["referenceExcerptSeconds"],
                        "durationFactor": profile["durationFactor"],
                        "emotionVector": profile["emotionVectorUI"], "emotionWeight": profile["emotionWeight"]}
        if sentence_mode:
            sample["segments"] = sentence_segments(scene, profile)
        samples.append(sample)
    plan = {"sourceId": profile["sourceId"], "profileId": profile["id"],
            "outputDirectory": str(output), "seed": profile["seed"],
            "generationParameters": profile["generationParameters"], "samples": samples,
            "userDirection": f"Selected B voice, light energy, duration {profile['durationFactor']}. Generation mode: {profile['generationMode']}."}
    if args.existing_plan:
        plan_path = Path(args.existing_plan).resolve()
        existing_plan = read_json(plan_path)
        if Path(existing_plan["outputDirectory"]).resolve() != output.resolve() or existing_plan["profileId"] != profile["id"]:
            raise RuntimeError("The existing batch must match the requested output and selected profile.")
    else:
        plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        runner = "run_indextts_rhythm_preview.py" if profile.get("generationMode") == "complete_sentences" else "run_indextts_preview_batch.py"
        subprocess.run([sys.executable, "-X", "utf8", str(TTS / "scripts" / runner),
                        "--plan", str(plan_path)], check=True)
    manifest_path = output / "batch-manifest.json"
    manifest = read_json(manifest_path)
    by_id = {sample["id"]: sample for sample in manifest["samples"]}
    asset_dir.mkdir(parents=True)
    timing = []
    fps = 30
    for scene in scenes:
        sample = by_id[scene["id"]]
        assert scene["id"] == sample["id"] and scene["say"] == sample["text"]
        assert sample["referenceSha256"] == profile["referenceSha256"]
        assert sample["durationFactor"] == profile["durationFactor"]
        assert sample["emotionVectorUI"] == profile["emotionVectorUI"] and sample["emotionWeight"] == profile["emotionWeight"]
        if sample.get("segments"):
            expected = sentence_segments(scene, profile)
            assert [part["text"] for part in expected] == [part["text"] for part in sample["segments"]]
            assert [part["pauseAfterMs"] for part in expected] == [part["addedPauseAfterMs"] for part in sample["segments"]]
            rate = sample["audio"]["sample_rate"]
            assert sample["audio"]["frames"] == sum(part["audio"]["frames"] + round(part["addedPauseAfterMs"] * rate / 1000) for part in sample["segments"])
        raw = Path(sample["audio"]["path"])
        audio_info = inspect_audio(raw)
        gain = min(0.08 / audio_info["rms"], 0.95 / audio_info["peak"])
        asset = asset_dir / f"{scene['id']}.wav"
        subprocess.run([str(TTS / "tools/ffmpeg/bin/ffmpeg.exe"), "-nostdin", "-hide_banner",
                        "-loglevel", "error", "-n", "-i", str(raw), "-af", f"volume={gain:.12f}",
                        "-c:a", "pcm_s16le", str(asset)], check=True)
        normalized = inspect_audio(asset)
        assert 0 < normalized["peak"] < 1
        assert normalized["frames"] == audio_info["frames"]
        duration = normalized["duration_seconds"]
        start_frame = 8
        cues = caption_cues(scene, sample, duration, start_frame, fps)
        timing.append({"id": scene["id"], "title": scene["title"],
                       "voiceSettings": settings,
                       "durationInFrames": start_frame + math.ceil(duration * fps) + 12,
                       "audioTracks": [{"text": scene["say"], "audio": asset.relative_to(VIDEO / "public").as_posix(),
                                        "frame": start_frame, "duration": duration}],
                       "captionAlignment": "measured_sentence_edges_with_estimated_internal_pages_pending_listening_review",
                       "cues": cues})
        sample["videoAsset"] = {**normalized, "sha256": hashlib.sha256(asset.read_bytes()).hexdigest(), "constantGain": gain}
        assert all(0 <= cue["startMs"] < cue["endMs"] <= timing[-1]["durationInFrames"] / fps * 1000 for cue in cues)
    if reused_timing:
        regenerated = {scene["id"]: scene for scene in timing}
        timing = [regenerated.get(scene["id"], reused_timing[scene["id"]]) for scene in all_scenes]
        manifest["reusedScenes"] = [scene for scene in timing if scene["id"] not in regenerated]
    manifest.update({"selectedReference": str(reference), "selectedProfile": profile_link["profilePath"],
                     "scriptStatus": "draft_awaiting_user_review", "manualPauseInsertion": profile["manualPauseInsertion"],
                     "sentencePauseMs": profile.get("sentencePauseMs", 0),
                     "videoTiming": str(VIDEO / "voiceover-timing.json"),
                     "captionAlignment": "measured_sentence_edges_with_estimated_internal_pages_pending_listening_review"})
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (VIDEO / "voiceover-timing.json").write_text(json.dumps(timing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    profile_link.update({"lastBatch": str(manifest_path), "pendingPlan": None,
                         "storyboardSha256": hashlib.sha256((VIDEO / "storyboard.json").read_bytes()).hexdigest()})
    (VIDEO / "voice-profile.json").write_text(json.dumps(profile_link, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # Match the review WAV to the exact scene boundaries without changing speech speed or pitch.
    import numpy as np
    import soundfile as sf
    rate = 22050
    pieces = []
    for scene in timing:
        track = scene["audioTracks"][0]
        wave, actual_rate = sf.read(VIDEO / "public" / track["audio"], dtype="float32", always_2d=True)
        assert actual_rate == rate and wave.shape[1] == 1
        count = round(scene["durationInFrames"] * rate / fps)
        offset = round(track["frame"] * rate / fps)
        assert offset + len(wave) <= count
        piece = np.zeros((count, 1), dtype="float32")
        piece[offset:offset + len(wave)] = wave * 0.9
        pieces.append(piece)
    review_path = output / "full-video-narration-review.wav"
    if review_path.exists():
        raise RuntimeError("The new batch already contains a review mix; do not overwrite it.")
    sf.write(review_path, np.concatenate(pieces), rate, subtype="PCM_16")
    report = {"batch": str(manifest_path), "scenes": len(timing),
              "durationInFrames": sum(scene["durationInFrames"] for scene in timing),
              "seconds": sum(scene["durationInFrames"] for scene in timing) / fps,
              "reviewAudio": inspect_audio(review_path), "speechSpeedOrPitchChangedInPost": False,
              "sentencePausesVerifiedFromPartFrameCounts": bool(profile["manualPauseInsertion"]),
              "subjectiveListeningReviewComplete": False}
    (VIDEO / "checks").mkdir(exist_ok=True)
    (VIDEO / "checks/voice-replacement-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
