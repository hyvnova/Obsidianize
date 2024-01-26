Bevy Version:0.9(outdated!)


Hot-Reloading Assets
Relevant official examples:
hot_asset_reloading.

At runtime, if you modify the file of an asset
that is loaded into the game (via the
AssetServer), Bevy can detect that and reload the
asset automatically. This is very useful for quick iteration. You can edit
your assets while the game is running and see the changes instantly in-game.
Not all file formats and use cases are supported
equally well. Typical asset types like textures / images should work without
issues, but complex GLTF or scene files, or assets involving custom logic,
might not.
If you need to run custom logic as part of your hot-reloading
workflow, you could implement it in a system, using
AssetEvent (learn more).
Hot reloading is opt-in and has to be enabled in order to work:
fn main() {
    App::new()
        .add_plugins(DefaultPlugins.set(AssetPlugin {
            watch_for_changes: true,
            ..Default::default()
        }))
        .run();
}
Note that this requires the filesystem_watcher Bevy cargo
feature. It is enabled by default, but if you have disabled
default features to customize Bevy, be sure to include it if you need it.
Shaders
Bevy also supports hot-reloading for shaders. You can edit your custom shader
code and see the changes immediately.
This works for any shader loaded from a file path, such as shaders specified
in your Materials definitions, or shaders loaded via the
AssetServer.
Shader code that does not come from asset files, such as if you include it
as a static string in your source code, cannot be hot-reloaded (for obvious
reasons).

### References
[[Asset Management  Unofficial Bevy Cheat Book]] [[List of Bevy Builtins  Unofficial Bevy Cheat Book]] [[Load Assets from Files  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[React to Changes with Asset Events  Unofficial Bevy Cheat Book]] [[Systems  Unofficial Bevy Cheat Book]] [[Customizing Bevy features modularity  Unofficial Bevy Cheat Book]] 