Bevy Version:0.11(outdated!)


Strange Build Errors
Sometimes, you can get strange and confusing build errors when trying to
compile your project.
Update your Rust
First, make sure your Rust is up-to-date. When using Bevy, you must use at
least the latest stable version of Rust (or nightly).
If you are using rustup to manage your Rust installation, you
can run:
rustup update

Clear the cargo state
Many kinds of build errors can often be fixed by forcing cargo to regenerate
its internal state (recompute dependencies, etc.). You can do this by deleting
the Cargo.lock file and the target directory.
rm -rf target Cargo.lock

Try building your project again after doing this. It is likely that the
mysterious errors will go away.
This trick often fixes the broken build, but if it doesn't help you,
your issue might require further investigation. Reach out to the Bevy
community via GitHub or Discord, and ask for help.
If you are using bleeding-edge Bevy ("main"), and the above does not solve
the problem, your errors might be caused by 3rd-party plugins. See this
page for solutions.
New Cargo Resolver
Cargo recently added a new dependency resolver algorithm, that is incompatible
with the old one. Bevy requires the new resolver.
If you are just creating a new blank Cargo project, don't worry. This should
already be setup correctly by cargo new.
If you are getting weird compiler errors from Bevy dependencies, read on. Make sure
you have the correct configuration, and then clear the cargo state.
Single-Crate Projects
In a single-crate project (if you only have one Cargo.toml file in your project),
if you are using the latest Rust2021 Edition, the new resolver is automatically
enabled.
So, you need either one of these settings in your Cargo.toml:
[package]
edition = "2021"

or
[package]
resolver = "2"

Multi-Crate Workspaces
In a multi-crate Cargo workspace, the resolver is a global setting for the
whole workspace. It will not be enabled by default.
This can bite you if you are transitioning a single-crate project into a workspace.
You must add it manually to the top-level Cargo.toml for your Cargo Workspace:
[workspace]
resolver = "2"

### References
[[Strange compile errors from Bevy or dependencies  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] 