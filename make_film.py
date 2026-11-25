#!/usr/bin/env python3
"""
Build the final Bisection Method film.

    intro (12.0 s) + scene1 (24.9) + scene2 (46.1) + theorem (24.5)
    + scene3 (45.2) + halving (22.6) + scene4 (44.7) + tolerance (18.9)
    + practice (23.6) + scene5 (41.1) -> about 304 s of 1080p60
    + macOS TTS narration (timed to the animation cues)
    + synthesized ambient bed (numpy), sidechain-ducked under the voice
    -> renders/Bisection_Method_Final_1080p60.mp4

Usage:  ./venv/bin/python make_film.py
"""

import pathlib
import subprocess
import wave

import numpy as np
from scipy.signal import lfilter

ROOT = pathlib.Path(__file__).resolve().parent
WORK = ROOT / "media" / "audio"
VO_DIR = WORK / "vo"
FINAL = ROOT / "renders" / "Bisection_Method_Final_1080p60.mp4"

SCENES = [
    ROOT / "media/videos/scene0_intro/1080p60/BisectionWelcome.mp4",
    ROOT / "media/videos/scene1_intro/1080p60/BisectionIntro.mp4",
    ROOT / "media/videos/scene2_concept/1080p60/BisectionConcept.mp4",
    ROOT / "media/videos/scene2b_ivt/1080p60/IvtTheorem.mp4",
    ROOT / "media/videos/scene3_iterations/1080p60/BisectionIterations.mp4",
    ROOT / "media/videos/scene3b_halving/1080p60/HalvingWhy.mp4",
    ROOT / "media/videos/scene4_convergence/1080p60/BisectionConvergence.mp4",
    ROOT / "media/videos/scene4b_tolerance/1080p60/ToleranceStop.mp4",
    ROOT / "media/videos/scene4c_significance/1080p60/InPractice.mp4",
    ROOT / "media/videos/scene5_conclusion/1080p60/BisectionConclusion.mp4",
]

VOICE = "Daniel"
RATE = 165  # words per minute; slower than the 175 default for a calmer read

# Intro cues, relative to the intro's own clock. The full sentence needs about
# 12 s of speech, so this block alone uses a brisker read (same voice) and each
# clip's trailing silence is trimmed to keep the opener near 12 s.
INTRO_RATE = 200
INTRO_NARRATION = [
    (0.15, "Hello everyone!", INTRO_RATE, 0.20),
    (1.27,
     "I am Muskaan Ramrakhyani from the Turing Batch, and today I will be "
     "explaining the Bisection Method.", INTRO_RATE, 0.20),
    (6.70,
     "Let's understand how this numerical method helps us find the roots of "
     "an equation, step by step.", INTRO_RATE, 0.20),
]

# (absolute start second, text). Cues follow the rendered animation timeline.
NARRATION = [
    (1.0, "Some equations cannot be solved by rearrangement."),
    (5.3, "So we study the shape of the function instead."),
    (9.9, "Its equation is x cubed, minus x, minus two."),
    (14.0, "Its root lies between one and two."),
    (17.4, "How do we find that root precisely, without solving the equation?"),
    (25.6, "The bisection method answers with a simple idea."),
    (29.3, "Start with an interval where the function changes sign."),
    (33.2, "At one, f is minus two. At two, f is plus four."),
    (37.7, "Opposite signs, so a root lies between them."),
    (41.6, "Step one: the interval from one to two."),
    (44.8, "Step two: the midpoint is a plus b over two. One point five."),
    (49.4, "Step three: evaluate the function at the midpoint."),
    (53.2, "f of one point five is minus zero point one two five."),
    (57.4, "Negative. But f of two is positive."),
    (60.6, "So the root stays in one point five to two."),
    (65.0, "Each pass halves the interval."),
]

# Bridge after scene 2: the Intermediate Value Theorem. Relative to its clock.
IVT_NARRATION = [
    (0.6, "Look at the two ends of the interval."),
    (2.65, "At x equals one, f of x is minus two: below the axis."),
    (7.4, "At x equals two, f of x is plus four: above the axis."),
    (13.15, "The curve is continuous, so it cannot jump over the axis."),
    (18.0, "To move from below to above, it must cross. A root is guaranteed inside."),
]

# Scene 3 starts after scenes 1 and 2; its cues are written relative to the
# scene's own clock and shifted by the offset measured at build time.
SCENE3_NARRATION = [
    (0.7, "Now we repeat the process."),
    (3.8, "The bracket is one point five to two: half a unit wide."),
    (8.4, "Midpoint one point seven five. f is positive, so the left half stays."),
    (15.0, "One point six two five. Still positive, so we keep the left half."),
    (21.9, "One point five six two five. Positive again."),
    (25.4, "Width: one eighth."),
    (28.7, "One point five three one two five. Barely positive."),
    (32.8, "Thirty one thousandths wide."),
    (35.9, "Each iteration halves the interval."),
    (38.6, "One half. A quarter. An eighth. Smaller and smaller."),
    (43.0, "The root is still inside."),
]

# Bridge after scene 3: why the interval halves every pass.
HALVING_NARRATION = [
    (2.0, "The midpoint splits the interval into two equal halves."),
    (5.6, "We test its sign, then keep the half where the sign still changes."),
    (10.2, "Only that half can still contain the root."),
    (13.0, "So every iteration cuts the width exactly in half."),
    (16.8, "After n steps, the width is b minus a, over two to the n."),
]

# Scene 4 cues are also relative to its own clock.
SCENE4_NARRATION = [
    (0.7, "Five iterations in, the bracket is tiny."),
    (4.0, "Each pass halved the width, down to one thirty-second."),
    (8.4, "The midpoint is our best estimate of the root."),
    (12.2, "And the error is at most half the width."),
    (16.1, "One more pass."),
    (17.5, "f of the midpoint is negative, so the root lies to the right."),
    (22.3, "Now the maximum error is under eight thousandths."),
    (26.2, "Our tolerance is one hundredth, so the test is passed."),
    (30.6, "Required accuracy achieved."),
    (33.3, "If we keep going, the bracket closes on the root."),
    (37.6, "Smaller interval. Smaller error. Better accuracy."),
]

# Bridge after scene 4: tolerance and the stopping criterion.
TOL_NARRATION = [
    (0.5, "Numerical methods never land exactly on the root."),
    (3.8, "So we decide how much error we can accept."),
    (6.8, "That limit is the tolerance, epsilon."),
    (9.7, "We stop once half the interval is smaller than epsilon."),
    (13.1, "With epsilon zero point zero one, the sixth pass is already enough."),
]

# Bridge after the tolerance panel: significance and limits.
SIG_NARRATION = [
    (0.5, "So where does bisection earn its place in practice?"),
    (4.1, "It needs no derivative: only continuity and a sign change."),
    (8.6, "That makes it a dependable fallback inside larger numerical software."),
    (13.1, "Its weakness is speed: each pass gains only one binary digit."),
    (17.6, "For fast results, it is often paired with Newton's method."),
]

# Scene 5 cues, relative to its own clock.
SCENE5_NARRATION = [
    (0.7, "Now, the final result."),
    (3.0, "The curve crosses the axis at a single point: the root."),
    (7.8, "x is approximately one point five two one three eight."),
    (12.5, "It is used across engineering, science and modelling."),
    (18.6, "Its strengths are simplicity and reliability."),
    (21.65, "But it converges slowly, and it needs a bracket."),
    (25.8, "Interval. Midpoint. Sign check. Keep the half. Repeat."),
    (30.72, "Simple, reliable, mathematically guaranteed."),
    (34.45, "Course M3, by Muskaan Ram Rakhyani."),
    (37.9, "Thank you for watching."),
]

SR = 48000


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def probe_duration(path):
    out = run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "csv=p=0", str(path),
    ]).stdout.strip()
    return float(out)


# ---------------------------------------------------------------- video
def build_video():
    video = WORK / "video_joined.mp4"
    listing = WORK / "video_list.txt"
    listing.write_text("".join(f"file '{p}'\n" for p in SCENES))
    joined = WORK / "video_joined_tmp.mp4"
    try:
        run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
             "-i", str(listing), "-c", "copy", str(joined)])
        ok = abs(probe_duration(joined) - sum(probe_duration(p) for p in SCENES)) < 0.2
    except subprocess.CalledProcessError:
        ok = False
    if not ok:
        run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
             "-i", str(listing), "-c:v", "libx264", "-preset", "slow",
             "-crf", "18", "-pix_fmt", "yuv420p", "-r", "60", str(joined)])
    joined.replace(video)
    return video


# ---------------------------------------------------------------- voice
def read_wav(path):
    with wave.open(str(path), "rb") as w:
        assert w.getnchannels() == 1 and w.getsampwidth() == 2
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    return data.astype(np.float32) / 32768.0


def write_wav(path, data, channels=1):
    data = np.clip(data, -1.0, 1.0)
    pcm = (data * 32767.0).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(channels)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def build_voice(length, narration):
    VO_DIR.mkdir(parents=True, exist_ok=True)
    track = np.zeros(int(length * SR) + SR, dtype=np.float32)

    print(f"{'#':>2}  {'start':>6}  {'end':>6}  {'len':>5}  text")
    spans = []
    for i, entry in enumerate(narration, 1):
        start, text = entry[0], entry[1]
        rate = entry[2] if len(entry) > 2 else RATE
        trim = entry[3] if len(entry) > 3 else 0.0
        raw = VO_DIR / f"line_{i:02d}.aiff"
        wav = VO_DIR / f"line_{i:02d}.wav"
        run(["say", "-v", VOICE, "-r", str(rate), "-o", str(raw), text])
        run(["ffmpeg", "-y", "-v", "error", "-i", str(raw),
             "-ar", str(SR), "-ac", "1", "-af",
             "highpass=f=90,equalizer=f=3200:t=q:w=1.2:g=2,"
             "acompressor=threshold=-20dB:ratio=3:attack=8:release=180:makeup=2dB",
             str(wav)])
        seg = read_wav(wav)
        if trim:
            seg = seg[: max(0, len(seg) - int(trim * SR))]
        # 8 ms edges so nothing clicks when segments are summed.
        edge = int(0.008 * SR)
        seg[:edge] *= np.linspace(0, 1, edge)
        seg[-edge:] *= np.linspace(1, 0, edge)
        at = int(start * SR)
        track[at:at + len(seg)] += seg
        end = start + len(seg) / SR
        spans.append((start, end, text))
        print(f"{i:>2}  {start:6.2f}  {end:6.2f}  "
              f"{len(seg) / SR:5.2f}  {text}")

    for (s0, e0, t0), (s1, _, t1) in zip(spans, spans[1:]):
        if e0 > s1 - 0.10:
            print(f"  !! line ending {e0:.2f} overruns next start {s1:.2f}: {t0!r}")

    peak = np.abs(track).max()
    track = track * (0.89 / peak)
    out = WORK / "voice.wav"
    write_wav(out, track)
    return out


# ---------------------------------------------------------------- music
def chord_pad(freqs, dur, sub_freq):
    n = int(dur * SR)
    t = np.arange(n) / SR
    attack, release = 4.0, 4.5
    env = np.ones(n)
    na, nr = int(attack * SR), int(release * SR)
    env[:na] = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, na))
    env[-nr:] *= 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, nr))

    left = np.zeros(n)
    right = np.zeros(n)
    for f in freqs:
        for detune, into in ((-0.0012, left), (0.0012, right)):
            fd = f * (1 + detune)
            tone = (np.sin(2 * np.pi * fd * t)
                    + 0.30 * np.sin(4 * np.pi * fd * t)
                    + 0.12 * np.sin(6 * np.pi * fd * t)
                    + 0.05 * np.sin(8 * np.pi * fd * t))
            into += tone * 0.5 / len(freqs)

    sub = np.sin(2 * np.pi * sub_freq * t) * 0.55 / len(freqs)
    left = (left + sub) * env
    right = (right + sub) * env
    return np.stack([left, right], axis=1)


def build_music(length):
    chords = [
        ([73.42, 110.00, 174.61, 293.66, 329.63], 36.71),   # Dm(add9)
        ([116.54, 174.61, 233.08, 293.66, 349.23], 58.27),  # Bbmaj7
        ([87.31, 130.81, 174.61, 220.00, 329.63], 43.65),   # Fmaj7
        ([130.81, 196.00, 261.63, 293.66, 392.00], 65.41),  # C(add9)
        ([73.42, 110.00, 174.61, 293.66, 369.99], 36.71),   # Dm(add9), open
        ([116.54, 174.61, 233.08, 293.66, 349.23], 58.27),  # Bbmaj7
        ([87.31, 130.81, 174.61, 220.00, 329.63], 43.65),   # Fmaj7
        ([130.81, 196.00, 261.63, 293.66, 392.00], 65.41),  # C(add9)
        ([73.42, 110.00, 174.61, 293.66, 369.99], 36.71),   # Dm(add9), close
    ]
    step, dur = 14.0, 20.0
    # Cover the whole film; entries 0-8 stay fixed so scenes 1-3 keep the bed
    # they were built with, then the cycle resumes and lands on a Dm close.
    cycle = chords[1:4] + [chords[0]]
    imax = int(np.ceil((length - dur) / step))
    while len(chords) - 1 < imax:
        chords.append(cycle[(len(chords) - 9) % 4])
    chords[-1] = chords[8]
    total = int(length * SR)
    mix = np.zeros((total, 2))

    rng = np.random.default_rng(7)
    for i, (freqs, sub) in enumerate(chords):
        seg = chord_pad(freqs, dur, sub)
        at = int(i * step * SR)
        end = min(at + len(seg), total)
        mix[at:end] += seg[:end - at]

    # Air: quiet band-limited noise, slowly swelling.
    n = total
    noise = rng.standard_normal(n)
    kernel = np.exp(-np.arange(int(0.0012 * SR)) / (0.00035 * SR))
    air = np.convolve(noise, kernel / kernel.sum(), mode="same") * 0.05
    t = np.arange(n) / SR
    air *= 0.5 + 0.5 * np.sin(2 * np.pi * 0.035 * t - 1.2)
    mix += air[:, None] * np.array([0.8, 1.0])

    # Soft stereo widening + smoothing via short delays.
    for delay_ms, gain, swap in ((23, 0.18, False), (37, 0.12, True)):
        d = int(delay_ms * 0.001 * SR)
        if swap:
            mix[d:, 0] += mix[:-d, 1] * gain
            mix[d:, 1] += mix[:-d, 0] * gain
        else:
            mix[d:, 0] += mix[:-d, 0] * gain
            mix[d:, 1] += mix[:-d, 1] * gain

    # Slow breathing and long fades.
    mix *= (0.86 + 0.14 * np.sin(2 * np.pi * 0.045 * t))[:, None]
    fade_in = int(2.5 * SR)
    fade_out = int(3.0 * SR)
    mix[:fade_in] *= np.linspace(0, 1, fade_in)[:, None] ** 1.5
    mix[-fade_out:] *= np.linspace(1, 0, fade_out)[:, None] ** 1.5

    mix *= 0.42 / np.abs(mix).max()
    raw = WORK / "music_raw.wav"
    write_wav(raw, mix, channels=2)
    out = WORK / "music.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(raw),
         "-af", "lowpass=f=2600:poles=2,highpass=f=32:poles=1", str(out)])
    return out


# ---------------------------------------------------------------- mix
def measure_lufs(path):
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af",
         "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    return float(proc.stderr.split("I:")[-1].split("LUFS")[0])


def duck(music, voice, depth_db=7.0, bed_gain_db=-12.0):
    """Envelope-following duck: full reduction while speech is present,
    smooth attack/release, no gain pumping between phrases."""
    sr = SR
    block = int(0.03 * sr)
    env = np.sqrt(np.convolve(voice.astype(np.float64) ** 2,
                              np.ones(block) / block, mode="same"))
    level = 20 * np.log10(env + 1e-9)
    # 0 below -40 dBFS, 1 above -28 dBFS
    amount = np.clip((level + 40) / 12, 0.0, 1.0)

    att = np.exp(-1 / (0.06 * sr))
    rel = np.exp(-1 / (0.18 * sr))
    smoothed = amount
    for a in (att, rel):
        smoothed = lfilter([1 - a], [1, -a], smoothed)

    gain = 10 ** ((bed_gain_db - depth_db * smoothed) / 20)
    return music * gain[:, None]


def build_mix(video, voice, music, length):
    sr = SR
    n = int(length * sr)

    with wave.open(str(music), "rb") as w:
        bed = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
        bed = bed.astype(np.float32).reshape(-1, 2) / 32768.0
    bed = bed[:n]
    if len(bed) < n:
        bed = np.pad(bed, ((0, n - len(bed)), (0, 0)))

    vo = read_wav(voice)[:n]
    if len(vo) < n:
        vo = np.pad(vo, (0, n - len(vo)))

    bed = duck(bed, vo)
    mix = bed + vo[:, None] * 0.95

    peak = np.abs(mix).max()
    mix *= 0.84 / peak
    raw = WORK / "mix.wav"
    write_wav(raw, mix, channels=2)

    # One static gain to the delivery target; if that would clip, stop at the
    # peak ceiling instead (no dynamic re-normalisation).
    loudness = measure_lufs(raw)
    peak_db = 20 * np.log10(np.abs(mix).max())
    gain_db = min(-16.0 - loudness, -1.0 - peak_db)
    out = WORK / "mix_norm.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(raw),
         "-af", f"volume={gain_db:.2f}dB,alimiter=limit=0.89:level=disabled",
         "-ar", str(sr), str(out)])
    print(f"mix: {loudness:.1f} LUFS -> {gain_db:+.1f} dB")
    return out


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    FINAL.parent.mkdir(parents=True, exist_ok=True)

    for scene in SCENES:
        if not scene.exists():
            raise SystemExit(f"missing render: {scene}")
    durations = [probe_duration(p) for p in SCENES]
    starts = []
    acc = 0.0
    for d in durations:
        starts.append(acc)
        acc += d
    length = acc
    narration = (
        INTRO_NARRATION
        + [(starts[1] + t, s) for t, s in NARRATION]
        + [(starts[3] + t, s) for t, s in IVT_NARRATION]
        + [(starts[4] + t, s) for t, s in SCENE3_NARRATION]
        + [(starts[5] + t, s) for t, s in HALVING_NARRATION]
        + [(starts[6] + t, s) for t, s in SCENE4_NARRATION]
        + [(starts[7] + t, s) for t, s in TOL_NARRATION]
        + [(starts[8] + t, s) for t, s in SIG_NARRATION]
        + [(starts[9] + t, s) for t, s in SCENE5_NARRATION]
    )
    print(f"film length: {length:.3f}s  (intro {durations[0]:.2f}s, "
          f"scene 1 at {starts[1]:.2f}s, theorem at {starts[3]:.2f}s, "
          f"scene 3 at {starts[4]:.2f}s, halving at {starts[5]:.2f}s, "
          f"scene 4 at {starts[6]:.2f}s, tolerance at {starts[7]:.2f}s, "
          f"practice at {starts[8]:.2f}s, scene 5 at {starts[9]:.2f}s)")

    print("joining scenes...")
    video = build_video()
    print("synthesizing narration...")
    voice = build_voice(length, narration)
    print("synthesizing music...")
    music = build_music(length)
    print("mixing...")
    mixed = build_mix(video, voice, music, length)

    run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-i", str(mixed),
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
         "-b:a", "192k", "-movflags", "+faststart", str(FINAL)])
    print(f"done: {FINAL}  ({probe_duration(FINAL):.2f}s)")


if __name__ == "__main__":
    main()
