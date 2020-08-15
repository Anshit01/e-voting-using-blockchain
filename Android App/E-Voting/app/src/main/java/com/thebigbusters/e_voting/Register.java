package com.thebigbusters.e_voting;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.Switch;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import java.util.HashMap;
import java.util.Map;

public class Register extends AppCompatActivity {
    EditText username, password, aadharnumber, contact, email, constituency;
    DatePicker datePicker;
    Button create;
    Switch notarobot;
    RequestQueue requestQueue;
    String BASE_URL = "";
    SharedPreferences sharedPreferences;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);
        username = findViewById(R.id.mainserver);
        password = findViewById(R.id.blockchain1);
        aadharnumber = findViewById(R.id.blockchain2);
        contact = findViewById(R.id.contact);
        email = findViewById(R.id.email);
        constituency = findViewById(R.id.Constituency);
        datePicker = findViewById(R.id.dateofbirth);
        create = findViewById(R.id.createuser);
        notarobot = findViewById(R.id.notarobot);
        requestQueue = Volley.newRequestQueue(this);
        sharedPreferences=getSharedPreferences(getString(R.string.pref),MODE_PRIVATE);
        BASE_URL=sharedPreferences.getString(getString(R.string.main),"");
        create.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                createuser();
            }
        });



    }


    private void createuser() {
        if (notarobot.isChecked()) {
            if (username.getEditableText().toString().equals("") || password.getEditableText().toString().equals("") || aadharnumber.getEditableText().toString().equals("")) {
                Toast.makeText(Register.this, "Fill all the fields", Toast.LENGTH_SHORT).show();
            } else {

                StringRequest makeuser = new StringRequest(Request.Method.POST, BASE_URL + "/create_user", new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                       if(response.equals("0")){
                           Toast.makeText(Register.this,"Please enter the correct information",Toast.LENGTH_LONG).show();
                       }
                       else {
                           Toast.makeText(Register.this,"Account created,Your key is "+response,Toast.LENGTH_LONG).show();
                           sharedPreferences.edit().putString(getString(R.string.key), response).apply();

                       }
                       finish();

                    }
                }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {

                    }
                }
                ) {
                    @Override
                    protected Map<String, String> getParams() {
                        Map<String, String> params = new HashMap<>();
                        params.put("name", username.getEditableText().toString());
                        params.put("aadhar_id", aadharnumber.getEditableText().toString());

                        int day = datePicker.getDayOfMonth();
                        int month = datePicker.getMonth() + 1;
                        int year = datePicker.getYear();

                        String date=year+"-"+month+"-"+day;


                        params.put("dob", date);
                        params.put("contact_no", contact.getEditableText().toString());
                        params.put("password",password.getEditableText().toString());
                        Log.d("TAG", "getParams: "+params);
                        Log.d("dob", "getParams: "+date);
                        return params;
                    }
                };


                requestQueue.add(makeuser);

            }

        }
        else
            Toast.makeText(Register.this,"You are a Robot",Toast.LENGTH_LONG).show();

    }


}
