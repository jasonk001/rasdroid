package itdm.droidplayer;

import android.content.Context;
import android.database.Cursor;
import android.view.View;
import android.widget.ImageView;

/**
 * This CursorBinder binds the provided image URL to an ImageView by downloading the image from the
 * Internet.
 */
public class UrlImageBinder extends Adapters.CursorBinder {

    private final ImageDownloader imageDownloader;

    public UrlImageBinder(Context context, Adapters.CursorTransformation transformation) {
        super(context, transformation);
        imageDownloader = new ImageDownloader();
    }

    @Override
    public boolean bind(View view, Cursor cursor, int columnIndex) {
        if (view instanceof ImageView) {
            String url = mTransformation.transform(cursor, columnIndex);
            url = "http://" + userPreferences.GetIPAddress(view.getContext()) + url;
            imageDownloader.download(url, (ImageView) view);
            return true;
        }

        return false;
    }
}
