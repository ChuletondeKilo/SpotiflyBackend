from pydantic import BaseModel
from typing import List, Optional, Union

class CreatePlaylistRequest(BaseModel):

    artists_ids: Union[list[str] | str]
    playlist_name: str

class artistList(BaseModel):

    artists_list: Union[str | list[str]]

class artistsSongs(BaseModel):

    artist: str
    songs: list[str]
    amonutSongs: int

class artistsSongsCollection(BaseModel):

    items: list[artistsSongs]

    def songsList(self):

        playlistSongList = []

        for item in self.items:

            playlistSongList += item.songs
        
        return playlistSongList

class artistSongList(BaseModel):
    artists_list: Union[str | list[str]]

class playlistResponse(BaseModel):
    playlistName: str
    playlistContent: artistsSongsCollection
