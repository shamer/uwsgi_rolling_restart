Simple python application to test/demonstrate rolling restarts of uWSGI.


Python Fooserv Servers
======================

Two different "versions" of the application fooserv exist in the directories ver_a and ver_b.

Both versions serve requests on /fast/ and /slow/. ver_a returns
201 responses to requests, ver_b returns 202 responses to all requests. The
/slow/ end point sleeps for between 3 and 6 seconds before serving the request.

Both servers do busy work for ~30 seconds on module import to simulate a slow
startup/initialization.


Initial Configuration
=====================

run ./rebuild_eggs.sh to create eggs for ver_a and ver_b
create symlink to build/eggs.pth in /usr/local/lib/python3.4/site-packages/rolling_restart_eggs.pth

The uWSGI configuration is adapted from The Zerg Dance section of The Art of
Graceful Reloading section of the documentation
<http://uwsgi-docs.readthedocs.org/en/latest/articles/TheArtOfGracefulReloading.html#zerg-mode>.


Testing
=======
start uwsgi zerg-server:
`uwsgi --ini conf/uwsgi_master.conf`

start first zerg instance in a new terminal
`uwsgi --ini conf/uwsgi_zerg.conf`

Start sieging to interogate the server
`siege -c 6 --file=<(echo "http://127.0.0.1:9090/slow/\nhttp://127.0.0.1:9090/fast/")`

switch the build symlink
`./switch_build.sh`

start replcement zerg instance in a new terminal
`uwsgi --ini conf/uwsgi_zerg.conf`

The new http status codes should show up in the siege output.

After a minute or two the first zerg instance can be killed
`echo q > run/sleeping.fifo`


Problems
========
If the UWSGI master process has any worker processes occational requests will
fail with "-- unavailable modifier requested: 0 --".

The hook-accepting1-once hook is run from by the worker process. This can race
with the master process spawning many workers. If the worker process runs the
hook first the writefifo call will be skipped and the zerg instance will never
transition over to the "running" fifo.

To work around this issue the writefifo can be replaced with an echo. The echo
will block until the master has opened the fifo.

