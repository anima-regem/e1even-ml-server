from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
import yt_dlp

app = FastAPI()

@app.get("/stream_song")
async def stream_song(search: str):
    search_query = f"{search}"
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'default_search': 'ytsearch',
        'writethumbnail': True,
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{search_query}", download=False)
            if 'entries' in info and info['entries']:
                # Take the first entry if available
                info = info['entries'][0]
                print(info)
                thumbnail_url = info.get('thumbnails', [{}])[0].get('url', '')
                thumbnail_url = thumbnail_url.replace('3', 'hqdefault')
                duration = info.get('duration', 0)
                artist_name = info.get('artist', '')
                file_info = {'title': info.get('title', ''), 
                    'url': info.get('url', ''),                    
                    'thumbnail_url': thumbnail_url,
                    'duration': duration,
                    'artist_name': artist_name,}
                return JSONResponse(content=file_info)
            else:
                raise HTTPException(status_code=500, detail="No matching video found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
