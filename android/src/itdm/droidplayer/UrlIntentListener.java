/*
 * Copyright (C) 2010 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package itdm.droidplayer;

import java.net.URLEncoder;

import itdm.droidplayer.playerHelper.ApiException;
import itdm.droidplayer.playerHelper.ParseException;

import android.content.Intent;

import android.view.Gravity;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.Toast;

/**
 * A listener which expects a URL as a tag of the view it is associated with. It then opens the URL
 * in the browser application.
 */
public class UrlIntentListener implements OnItemClickListener {

    public Boolean removeFromList = false;
    
    
	public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
        
        playerHelper.prepareUserAgent(view.getContext());
        
        String text = "";
        try {
			if(removeFromList)
			{
				if(position > 0)
				{
					playerHelper.removeFromPlayList(parent.getContext(),Integer.toString(position));
					text = parent.getContext().getString(R.string.msg_track_removed);
					
					//reload the now playing list
					Intent nowplayingIntent = new Intent(parent.getContext(),nowplayingReaderActivity.class);
	            	nowplayingIntent.setFlags(Intent.FLAG_ACTIVITY_NO_HISTORY);
	            	parent.getContext().startActivity(nowplayingIntent);
				}
				else
				{
					text = parent.getContext().getString(R.string.msg_cant_remove);
				}
				
			}
			else
			{
				//if we aren't remove it then we are adding it to the play list
				final String url = view.getTag().toString();
				
				playerHelper.addToPlayList(parent.getContext(),URLEncoder.encode(url));
				
				text = parent.getContext().getString(R.string.msg_track_added);
			}
			
			//display a message to the user
			int duration = Toast.LENGTH_SHORT;

			Toast toast = Toast.makeText(view.getContext(), text, duration);
			toast.setGravity(Gravity.CENTER_VERTICAL, 0, 0);
			toast.show();
			
		} catch (ApiException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (ParseException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
  
    }

}
