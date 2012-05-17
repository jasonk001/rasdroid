package itdm.droidplayer;

import android.os.Bundle;

import android.widget.AdapterView.OnItemClickListener;

/**
 * This example demonstrate the creation of a simple RSS feed reader using the XML adapter syntax.
 * The different elements of the feed are extracted using an {@link XmlDocumentProvider} and are
 * binded to the different views. An {@link OnItemClickListener} is also added, which will open a
 * browser on the associated news item page.
 */
public class nowplayingReaderActivity extends baseMenuActivity {
	private static final String NOWPLAYING_URI = "content://xmldocument/?url=http://%s/currentplaylist.php";
    
	private String GetNowPlayingURI()
	{
		
		return String.format( NOWPLAYING_URI,userPreferences.GetIPAddress(this));
	}

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        setContentView(R.layout.nowplaying_list);
         
        setListAdapter(Adapters.loadCursorAdapter(this, R.xml.nowplaying_feed,
        		GetNowPlayingURI()));
        
        UrlIntentListener newListener = new UrlIntentListener();
        
        newListener.removeFromList = true;
        
        getListView().setOnItemClickListener(newListener);
        
    }
   
}