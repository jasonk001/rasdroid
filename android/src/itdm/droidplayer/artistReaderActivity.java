package itdm.droidplayer;
import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.net.URLConnection;

import org.apache.http.util.ByteArrayBuffer;


import android.os.Bundle;


public class artistReaderActivity extends baseMenuActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        try{
        	
        	File file = new File(super.ARTIST_LOCAL_PATH);
	        
        	//if the file doesn't exist then download it
        	if(!file.exists())
	        	{
		        	URL url = new URL(super.GetArtistFeedURI());
		        
		        	URLConnection ucon = url.openConnection();
		        	
		        	InputStream is = ucon.getInputStream();
		            BufferedInputStream bis = new BufferedInputStream(is);
		            ByteArrayBuffer baf = new ByteArrayBuffer(50);
		            int current = 0;
		            while ((current = bis.read()) != -1) {
		                    baf.append((byte) current);
		            }
		
		            // Convert the Bytes read to a String.
		            FileOutputStream fos = new FileOutputStream(file);
		            fos.write(baf.toByteArray());
		            fos.close();
	        	}
        	} catch (IOException e){}
	    
        setContentView(R.layout.artist_list);

        String uriPath = "content://xmldocument/" + super.ARTIST_FILE_URI; 
        setListAdapter(Adapters.loadCursorAdapter(this, R.xml.artist_feed,
        		uriPath));
        GroupIntentListener newListener = new GroupIntentListener();
        newListener.listType = "artist";
        getListView().setOnItemClickListener(newListener);
    }
    
   
    
}