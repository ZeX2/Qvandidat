
# Cloning

When cloning use the `--recursive` option to ensure that all submodules are cloned,

`git clone --recursive [URL to repository]`.


# Initializing a cloned repository

If the repository is cloned but the submodules missing (submodule folders are empty) then initialize the submodules using

`git submodule update --init --recursive`.


# Updating submodules

Sometimes submodules are updated, to sync those updates run
`git submodule update --recursive --remote`
or
`git pull --recurse-submodules`.

