package com.carbon;

import android.os.Bundle;

import com.phonegap.*;

public class MainActivity extends DroidGap {
    /** Called when the activity is first created. */
    public void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        super.loadUrl("file:///android_asset/www/index.html");

    }
}