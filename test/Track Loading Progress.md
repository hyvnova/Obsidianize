Bevy Version:0.9(outdated!)


Track Loading Progress
There are good community plugins that can help with this. Otherwise, this page
shows you how to do it yourself.

If you want to check the status of various asset files,
you can poll it from the AssetServer. It will tell you
whether the asset(s) are loaded, still loading, not loaded, or encountered
an error.
To check an individual asset, you can use asset_server.get_load_state(…) with
a handle or path to refer to the asset.
To check a group of many assets, you can add them to a single collection
(such as a Vec<HandleUntyped>; untyped handles are very
useful for this) and use asset_server.get_group_load_state(…).

Here is a more complete code example:
#[derive(Resource)]
struct AssetsLoading(Vec<HandleUntyped>);

fn setup(server: Res<AssetServer>, mut loading: ResMut<AssetsLoading>) {
    // we can have different asset types
    let font: Handle<Font> = server.load("my_font.ttf");
    let menu_bg: Handle<Image> = server.load("menu.png");
    let scene: Handle<Scene> = server.load("level01.gltf#Scene0");

    // add them all to our collection for tracking
    loading.0.push(font.clone_untyped());
    loading.0.push(menu_bg.clone_untyped());
    loading.0.push(scene.clone_untyped());
}

fn check_assets_ready(
    mut commands: Commands,
    server: Res<AssetServer>,
    loading: Res<AssetsLoading>
) {
    use bevy::asset::LoadState;

    match server.get_group_load_state(loading.0.iter().map(|h| h.id)) {
        LoadState::Failed => {
            // one of our assets had an error
        }
        LoadState::Loaded => {
            // all assets are now ready

            // this might be a good place to transition into your in-game state

            // remove the resource to drop the tracking handles
            commands.remove_resource::<AssetsLoading>();
            // (note: if you don't have any other handles to the assets
            // elsewhere, they will get unloaded after this)
        }
        _ => {
            // NotLoaded/Loading: not fully ready yet
        }
    }
}

### References
[[Handles  Unofficial Bevy Cheat Book]] [[Load Assets from Files  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] 