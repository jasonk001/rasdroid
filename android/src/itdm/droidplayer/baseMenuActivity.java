package itdm.droidplayer;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.net.URLConnection;

import org.apache.http.util.ByteArrayBuffer;

import android.app.ListActivity;
import android.content.Intent;
import android.view.Gravity;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.widget.Toast;

public abstract class baseMenuActivity extends ListActivity{
	protected final String ALBUM_LOCAL_PATH = "/data/data/itdm.droidplayer/albums.xml";
	protected final String ARTIST_LOCAL_PATH = "/data/data/itdm.droidplayer/artists.xml";
	private final String ARTIST_FEED_URI = "http://%s/artists.xml";
	private final String ALBUM_FEED_URI = "http://%s/albums.xml";
	protected final String ALBUM_FILE_URI = "content://xmldocument/?file=albums.xml";
	protected final String ARTIST_FILE_URI = "content://xmldocument/?file=artists.xml";
		
	protected String GetArtistFeedURI()
		{
			return String.format( ARTIST_FEED_URI, userPreferences.GetIPAddress(this));
		}
	
	protected String GetAlbumFeedURI()
	{
		return String.format( ALBUM_FEED_URI, userPreferences.GetIPAddress(this));
	}
	
		@Override
	    public boolean onCreateOptionsMenu(Menu menu) {
	        MenuInflater inflater = getMenuInflater();
	        inflater.inflate(R.menu.player_menu, menu);
	        return true;
	    }
	    @Override
	    public boolean onOptionsItemSelected(MenuItem item) {
	        // Handle item selection
	        switch (item.getItemId()) {
	            case R.id.menu_albums:
	            	Intent albumintent = new Intent(this,albumReaderActivity.class);
	            	//albumintent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
	            	albumintent.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
	            	startActivity( albumintent );
	            	
	                return true;
	            case R.id.menu_artists:
	            	Intent artistIntent = new Intent(this,artistReaderActivity.class);
	            	artistIntent.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
	            	startActivity(artistIntent);
	                return true;
	            case R.id.menu_nowplaying:
	            	Intent nowplayingIntent = new Intent(this,nowplayingReaderActivity.class);
	            	nowplayingIntent.setFlags(Intent.FLAG_ACTIVITY_NO_HISTORY);
	            	startActivity(nowplayingIntent);
	                return true;
	            case R.id.menu_settings:
	            	Intent settingsIntent = new Intent(this,settingsActivity.class);
	            	
	            	startActivity(settingsIntent);
	                return true;
	            case R.id.menu_sync:
	            	
	            		//delete the files
	            		File delFile = new File(ALBUM_LOCAL_PATH);
	            		delFile.delete();
	            		
	            		delFile = new File(ARTIST_LOCAL_PATH);
	            		delFile.delete();
	            	
	                
	            	try{
	                	
	            		File file = new File(ALBUM_LOCAL_PATH);
	        	        
	                	//if the file doesn't exist then download it
	                	if(!file.exists())
	        	        	{
	        		        	URL url = new URL(ALBUM_FEED_URI);
	        		        	CacheFeed(url, file);
	        		        }
	                	
	                	file = new File(ARTIST_LOCAL_PATH);
	                	
	                	if(!file.exists())
        	        	{
        		        	URL url = new URL(ARTIST_FEED_URI);
        		        	CacheFeed(url, file);
        		        }
	                	
	                	} catch (IOException e){}
	                	
	                	//Display a message to the user
	                	
	                	int duration = Toast.LENGTH_SHORT;

	        			Toast toast = Toast.makeText(this, R.string.msg_media_updated, duration);
	        			toast.setGravity(Gravity.CENTER_VERTICAL, 0, 0);
	        			toast.show();
	        			
	                	//reload the current activity to ensure that any new tracks are displayed
	        			Intent currentIntent = new Intent(this,this.getClass());
	                	currentIntent.setFlags(Intent.FLAG_ACTIVITY_NO_HISTORY);
	                	startActivity(currentIntent);
	                	finish();
	                	
	            	return true;
	            default:
	                return super.onOptionsItemSelected(item);
	        }
	    }
	    
	    private void CacheFeed(URL url, File file)
	    {
		    try
		    {
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
		    }catch (IOException e){}
		
	    }
}
