import os
import subprocess
import yt_dlp


def buat_klip_otomatis(url_video, mulai_detik=15, durasi=45, hook_text=""):
    temp_video = "temp_video.mp4"
    output_file = "klip_viral_9x16.mp4"

    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "outtmpl": temp_video,
        "merge_output_format": "mp4",
    }

    if os.path.exists("cookies.txt") and os.path.getsize("cookies.txt") > 10:
        print("Menggunakan cookies.txt...")
        ydl_opts["cookiefile"] = "cookies.txt"
    else:
        print("PERINGATAN: cookies.txt tidak ditemukan atau kosong!")

    try:
        print(f"Mengunduh video dari: {url_video}...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url_video])

        clean_hook = (hook_text or "").replace("'", "\\'").replace(":", "\\:")
        if clean_hook:
            vf_filter = (
                f"crop=ih*(9/16):ih,scale=1080:1920,"
                f"drawtext=text='{clean_hook}':fontcolor=white:fontsize=46:"
                f"box=1:boxcolor=black@0.65:boxborderw=16:"
                f"x=(w-text_w)/2:y=180:enable='between(t,0,5)'"
            )
        else:
            vf_filter = "crop=ih*(9/16):ih,scale=1080:1920"

        print("Memotong dan mengubah rasio ke 9:16...")
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(mulai_detik),
            "-i", temp_video,
            "-t", str(durasi),
            "-vf", vf_filter,
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k",
            output_file,
        ]
        subprocess.run(cmd, check=True)
        print(f"Selesai! Output tersimpan di: {output_file}")
    finally:
        if os.path.exists(temp_video):
            os.remove(temp_video)
            print(f"File sementara {temp_video} dibersihkan.")


if __name__ == "__main__":
    url = os.environ.get("VIDEO_URL")
    mulai = int(os.environ.get("MULAI_DETIK", "15"))
    durasi = int(os.environ.get("DURASI", "45"))
    hook = os.environ.get("HOOK_TEXT", "")

    if not url:
        raise ValueError("VIDEO_URL wajib diisi!")

    buat_klip_otomatis(url_video=url, mulai_detik=mulai, durasi=durasi, hook_text=hook)
