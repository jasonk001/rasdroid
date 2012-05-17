package itdm.droidplayer;

import android.app.Activity;
import android.content.SharedPreferences;
import android.os.Bundle;

import android.widget.TextView;


public class settingsActivity extends Activity {
	private static final String PREFS_NAME = "DroidPlayerPrefsFile";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.settings);
     
        //load the preferences
        SharedPreferences settings = getSharedPreferences(PREFS_NAME, 0);
        String ipAddress = settings.getString("ipaddress", "");
        TextView ipaddressView = (TextView)findViewById(R.id.ipaddress);
        ipaddressView.setText(ipAddress);
        
    }
    
    @Override
    protected void onStop(){
       super.onStop();
     
       try
       {
       SharedPreferences settings = getSharedPreferences(PREFS_NAME, 0);
       SharedPreferences.Editor editor = settings.edit();
       TextView ipaddressView = (TextView)findViewById(R.id.ipaddress);
       String ipaddress = ipaddressView.getText().toString();
       editor.putString("ipaddress",ipaddress);
       // Commit the edits!
       editor.commit();
       }catch(Exception e){}
       
    }
   
}