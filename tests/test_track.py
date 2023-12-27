import os
import shutil

from util import arun

from streamrip.client.downloadable import Downloadable
from streamrip.client.qobuz import QobuzClient
from streamrip.media.track import PendingSingle, Track
import streamrip.db as db
from fixtures.clients import qobuz_client


def test_pending_resolve(qobuz_client: QobuzClient):
    qobuz_client.config.session.downloads.folder = "./tests"
    p = PendingSingle("19512574", qobuz_client, qobuz_client.config, db.Database(db.Dummy(), db.Dummy()))
    t = arun(p.resolve())
    dir = "tests/tests/Fleetwood Mac - Rumours (1977) [FLAC] [24B-96kHz]"
    assert os.path.isdir(dir)
    assert os.path.isfile(os.path.join(dir, "cover.jpg"))
    #embedded_cover_path aka t.cover_path is
    #./tests/./tests/Fleetwood Mac - Rumours (1977) [FLAC] [24B-96kHz]/
    # __artwork/cover-9202762427033526105.jpg
    assert os.path.isfile(t.cover_path)
    assert isinstance(t, Track)
    assert isinstance(t.downloadable, Downloadable)
    assert t.cover_path is not None
    shutil.rmtree(dir)


# def test_pending_resolve_mp3(qobuz_client: QobuzClient):
#     qobuz_client.config.session.qobuz.quality = 1
#     p = PendingSingle("19512574", qobuz_client, qobuz_client.config)
#     t = arun(p.resolve())
#     assert isinstance(t, Track)
#     assert False
