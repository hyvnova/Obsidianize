Bevy Version:0.9(outdated!)


Access the Asset Data
To access the actual asset data from systems, use the
Assets<T> resource.
You can identify your desired asset using the handle.
untyped handles need to be "upgraded" into typed handles.
#[derive(Resource)]
struct SpriteSheets {
    map_tiles: Handle<TextureAtlas>,
}

fn use_sprites(
    handles: Res<SpriteSheets>,
    atlases: Res<Assets<TextureAtlas>>,
    images: Res<Assets<Image>>,
) {
    // Could be `None` if the asset isn't loaded yet
    if let Some(atlas) = atlases.get(&handles.map_tiles) {
        // do something with the texture atlas
    }
}
Creating Assets from Code
You can also add assets to Assets<T> manually.
Sometimes you need to create assets from code, rather than loading them
from files. Some common examples of such use-cases are:

creating texture atlases
creating 3D or 2D materials
procedurally-generating assets like images or 3D meshes

To do this, first create the data for the asset (an instance of the
asset type), and then add it .add(…) it to the
Assets<T> resource, for it to be stored and tracked by
Bevy. You will get a handle to use to refer to it, just like
any other asset.
fn add_material(
    mut materials: ResMut<Assets<StandardMaterial>>,
) {
    let new_mat = StandardMaterial {
        base_color: Color::rgba(0.25, 0.50, 0.75, 1.0),
        unlit: true,
        ..Default::default()
    };

    let handle = materials.add(new_mat);

    // do something with the handle
}

### References
[[Load Assets from Files  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Handles  Unofficial Bevy Cheat Book]] [[Resources  Unofficial Bevy Cheat Book]] [[List of Bevy Builtins  Unofficial Bevy Cheat Book]] [[Handles  Unofficial Bevy Cheat Book]] 