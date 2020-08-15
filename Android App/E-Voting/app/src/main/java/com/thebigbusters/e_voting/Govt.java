package com.thebigbusters.e_voting;

import androidx.appcompat.app.AppCompatActivity;

import android.app.DownloadManager;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import com.android.volley.RequestQueue;
import com.android.volley.toolbox.Volley;

public class Govt extends AppCompatActivity {
    EditText username,password,aadharnumber,key;
    Button vote,liveresult,candiateslist,register;
    SharedPreferences sharedPreferences;

    RequestQueue requestQueue;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_govt);

        username=findViewById(R.id.mainserver);
        password=findViewById(R.id.blockchain1);
        aadharnumber=findViewById(R.id.blockchain2);
        key=findViewById(R.id.blockchain3);
        vote=findViewById(R.id.castvote);
        liveresult=findViewById(R.id.livestats);
        candiateslist=findViewById(R.id.list);
        register=findViewById(R.id.register);
        sharedPreferences=getSharedPreferences(getString(R.string.pref),MODE_PRIVATE);
        key.setText(sharedPreferences.getString(getString(R.string.key),""));
        requestQueue= Volley.newRequestQueue(this);



        vote.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                castvote();
            }
        });

        register.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(Govt.this,Register.class));
                finish();
            }
        });

        candiateslist.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(Govt.this,CandidateList.class));
                finish();
            }
        });
        liveresult.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(Govt.this,live_stats.class));
                finish();
            }
        });

    }


    private void castvote(){

        Intent i =new Intent(Govt.this,CandidateList.class);
        i.putExtra("voting", true);
        i.putExtra("name",username.getEditableText().toString());
        i.putExtra("password",password.getEditableText().toString());
        i.putExtra("aadhar",aadharnumber.getEditableText().toString());
        i.putExtra("key",key.getEditableText().toString());
        startActivity(i);
        finish();

    }



}
