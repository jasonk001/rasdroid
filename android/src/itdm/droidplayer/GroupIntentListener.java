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


import android.content.Intent;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;

/**
 * A listener which expects a URL as a tag of the view it is associated with. It then opens the URL
 * in the browser application.
 */
public class GroupIntentListener implements OnItemClickListener {
	
	public String listType = "";
	
    public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
        final String itemid = view.getTag().toString();
        
		final Intent intent = new Intent(parent.getContext(),trackListActivity.class);
		
		intent.putExtra(listType + "id", itemid);
		
		parent.getContext().startActivity(intent);

    }

}
