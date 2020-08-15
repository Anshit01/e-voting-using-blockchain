package com.thebigbusters.e_voting;

import androidx.appcompat.app.AppCompatActivity;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class setting extends AppCompatActivity {
    EditText main,block1,block2,block3;
    Button save;
    SharedPreferences sharedPreferences;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_setting);
        main=findViewById(R.id.mainserver);
        block1=findViewById(R.id.blockchain1);
        block2=findViewById(R.id.blockchain2);
        block3=findViewById(R.id.blockchain3);
        save=findViewById(R.id.save);
        sharedPreferences=getSharedPreferences(getString(R.string.pref),MODE_PRIVATE);

        main.setText(sharedPreferences.getString(getString(R.string.main),""));
        block1.setText(sharedPreferences.getString(getString(R.string.block),""));
        block2.setText(sharedPreferences.getString(getString(R.string.block2),""));
        block3.setText(sharedPreferences.getString(getString(R.string.block3),""));

        save.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sharedPreferences.edit().putString(getString(R.string.main),main.getEditableText().toString()).apply();
                sharedPreferences.edit().putString(getString(R.string.block),block1.getEditableText().toString()).apply();
                sharedPreferences.edit().putString(getString(R.string.block2),block2.getEditableText().toString()).apply();
                sharedPreferences.edit().putString(getString(R.string.block3),block3.getEditableText().toString()).apply();
            }
        });



    }
}
