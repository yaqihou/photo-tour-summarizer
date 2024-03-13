
import os
import time
import pickle

from .defs import Wallpaper 
from ..logger import MyLogger

logger = MyLogger('data-fetch-utils.wallhaven.cacher')

class Cache:

    _cache_file = os.path.join(os.getenv('HOME') or '.',
                              '.cache',
                              'data-fetch-utils',
                              'wallhaven_downloaded.pkl')

    if os.path.isfile(_cache_file):
        with open(_cache_file, 'rb') as f:
            _cache = pickle.load(f)
    else:
        _cache = {}

    def __init__(self):
        logger.debug(f'Loaded {len(self._cache)} entries from cache file {self._cache_file}')

    def __len__(self):
        return len(self._cache)

    def __contains__(self, val: str):
        return val in self._cache

    def __getitem__(self, key: str):
        return self._cache[key]

    def add(self, wallpaper: Wallpaper):
        self._cache[wallpaper.id] = wallpaper.json

    def fetch_wallpaper(self, wid) -> Wallpaper:
        # let it crash
        return Wallpaper(self._cache[wid])

    def save(self):
        dirname = os.path.dirname(self._cache_file)
        if not os.path.isdir(dirname):
            logger.debug(f'Cache folder {dirname} does not exist, create one')
            os.makedirs(dirname)

        with open(self._cache_file, 'wb') as f:
            pickle.dump(self._cache, f)
            logger.debug(f'Saved {len(self._cache)} cached entries to {self._cache_file}')
