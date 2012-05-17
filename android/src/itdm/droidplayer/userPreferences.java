package itdm.droidplayer;

import android.content.Context;
import android.content.SharedPreferences;

public class userPreferences {
	
	protected static final String PREFS_NAME = "DroidPlayerPrefsFile";
	
	public static String GetIPAddress(Context context){
		
		SharedPreferences settings = context.getSharedPreferences(PREFS_NAME, 0);
        return settings.getString("ipaddress", "");
		
	}

}
