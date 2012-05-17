package itdm.droidplayer;



import android.os.Bundle;

import android.widget.AdapterView.OnItemClickListener;

/**
 * This example demonstrate the creation of a simple RSS feed reader using the XML adapter syntax.
 * The different elements of the feed are extracted using an {@link XmlDocumentProvider} and are
 * binded to the different views. An {@link OnItemClickListener} is also added, which will open a
 * browser on the associated news item page.
 */
public class trackListActivity extends baseMenuActivity {
    private static final String ALBUM_URI = "content://xmldocument/?url=http://192.168.200.131/albums/";
    private static final String ARTIST_URI = "content://xmldocument/?url=http://192.168.200.131/artists/";
       
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
	    
        setContentView(R.layout.track_list);
        Bundle extras = getIntent().getExtras();
        
  	  	if(extras !=null)
  	  	{
  	  		String albumid = extras.getString("albumid");
  	  		String artistid = extras.getString("artistid");
  	  		String uriPath = "";
  	  		if(albumid != null)
  	  		{
  	  			uriPath = ALBUM_URI + albumid + ".xml";
  	  			setListAdapter(Adapters.loadCursorAdapter(this, R.xml.album_track_feed,
					uriPath));
        		
  	  		}
  	  		else
  	  		{
  	  			uriPath = ARTIST_URI + artistid + ".xml";
  	  		setListAdapter(Adapters.loadCursorAdapter(this, R.xml.artist_track_feed,
					uriPath));
  	  		}
  	  		
  	  		
  	  		
  	  		
  	  		
  	  		getListView().setOnItemClickListener(new UrlIntentListener());
  	  	}
        
    }
   
    
    
}