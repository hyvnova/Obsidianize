Bevy Version:0.12(current)


Getting Started
This page covers the basic setup needed for Bevy development.

For the most part, Bevy is just like any other Rust library. You need to
install Rust and setup your dev environment just like for any other Rust
project. You can install Rust using Rustup. See
Rust's official setup page.
On Linux, you need the development files for some system libraries. See the
official Bevy Linux dependencies page.
Also see the Setup page in the official Bevy Book
and the official Bevy Readme.
Creating a New Project
You can simply create a new Rust project, either from your IDE/editor, or the commandline:
cargo new --bin my_game

(creates a project called my_game)
The Cargo.toml file contains all the configuration of your project.
Add the latest version of bevy as a dependency. Your file should now
look something like this:
[package]
name = "my_game"
version = "0.1.0"
edition = "2021"

[dependencies]
bevy = "0.12"

The src/main.rs file is your main source code file. This is where you
start writing your Rust code. For a minimal Bevy app, you need
at least the following:
use bevy::prelude::*;

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .run();
}
You can now compile and run your project. The first time, this will take a
while, as it needs to build the whole Bevy engine and dependencies. Subsequent
runs should be fast. You can do this from your IDE/editor, or the commandline:
cargo run

Documentation
You can generate your own docs (like what is on docs.rs), for
offline use, including everything from your own project and all dependencies, in
one place.
cargo doc --open

This will build all the HTML docs and open them in your web browser.
It does not require an internet connection, and gives you an easy way to search
the API docs for all crates in your dependency tree all at once. It is more
useful than the online version of the docs.
Optional Extra Setup
You will likely quickly run into unusably slow performance with the default
Rust unoptimized dev builds. See here how to fix.
Iterative recompilation speed is important to keep you productive, so you don't
have to wait long for the Rust compiler to rebuild your project every time you
want to test your game. Bevy's getting started page
has advice about how to speed up compile times.
Also have a look in the Dev Tools and Editors page for suggestions
about additional external dev tools that may be helpful.
What's Next?
Have a look at the guided tutorial page of this book,
and Bevy's official examples.
Check out the Bevy Assets Website to find other tutorials
and learning resources from the community, and plugins
to use in your project.
Join the community on Discord to chat with us!
Running into Issues?
If something is not working, be sure to check the Common
Pitfalls chapter, to see if this book has something to
help you. Solutions to some of the most common issues that Bevy community
members have encountered are documented there.
If you need help, use GitHub Discussions, or feel
welcome to come chat and ask for help in Discord.
GPU Drivers
To work at its best, Bevy needs DirectX 12 (Windows) or Vulkan (Linux, Android,
Windows). macOS/iOS should just work, without any special driver setup, using
Metal.
OpenGL (GLES3) can be used as a fallback, but will likely have issues (some
bugs, unsupported features, worse performance).
Make sure you have compatible hardware and drivers installed on your system.
Your users will also need to satisfy this requirement.
If Bevy is not working, install the latest drivers for your OS, or check with
your Linux distribution whether Vulkan needs additional packages to be
installed.
Web games are supported and should work in any modern browser, using WebGL2.
Performance is limited and some Bevy features will not work. The new
experimental high-performance WebGPU API is also supported, but browser adoption
is still limited.

### References
[[Common Pitfalls  Unofficial Bevy Cheat Book]] [[Bevy Tutorials  Unofficial Bevy Cheat Book]] [[Dev Tools and Editors for Bevy  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Community Plugin Ecosystem  Unofficial Bevy Cheat Book]] [[The App  Unofficial Bevy Cheat Book]] [[Slow Performance  Unofficial Bevy Cheat Book]] 