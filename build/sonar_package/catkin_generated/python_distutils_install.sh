#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/ubuntu/spring-2023-ros-workspace/src/sonar_package"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/ubuntu/spring-2023-ros-workspace/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/ubuntu/spring-2023-ros-workspace/install/lib/python3/dist-packages:/home/ubuntu/spring-2023-ros-workspace/build/sonar_package/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/ubuntu/spring-2023-ros-workspace/build/sonar_package" \
    "/usr/bin/python3" \
    "/home/ubuntu/spring-2023-ros-workspace/src/sonar_package/setup.py" \
     \
    build --build-base "/home/ubuntu/spring-2023-ros-workspace/build/sonar_package" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/ubuntu/spring-2023-ros-workspace/install" --install-scripts="/home/ubuntu/spring-2023-ros-workspace/install/bin"
