Bevy Version:0.9(outdated!)


React to Changes with Asset Events
If you need to perform specific actions when an asset is created,
modified, or removed, you can make a system that reacts to
AssetEvent events.
#[derive(Resource)]
struct MyMapImage {
    handle: Handle<Image>,
}

fn fixup_images(
    mut ev_asset: EventReader<AssetEvent<Image>>,
    mut assets: ResMut<Assets<Image>>,
    map_img: Res<MyMapImage>,
) {
    for ev in ev_asset.iter() {
        match ev {
            AssetEvent::Created { handle } => {
                // a texture was just loaded or changed!

                // WARNING: this mutable access will cause another
                // AssetEvent (Modified) to be emitted!
                let texture = assets.get_mut(handle).unwrap();
                // ^ unwrap is OK, because we know it is loaded now

                if *handle == map_img.handle {
                    // it is our special map image!
                } else {
                    // it is some other image
                }
            }
            AssetEvent::Modified { handle } => {
                // an image was modified
            }
            AssetEvent::Removed { handle } => {
                // an image was unloaded
            }
        }
    }
}
Note: If you are handling Modified events and doing a mutable access to
the data, the .get_mut will trigger another Modified event for the same
asset. If you are not careful, this could result in an infinite loop! (from
events caused by your own system)

### References
[[Systems  Unofficial Bevy Cheat Book]] [[Events  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] 