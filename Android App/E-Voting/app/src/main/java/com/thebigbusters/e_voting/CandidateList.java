package com.thebigbusters.e_voting;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class CandidateList extends AppCompatActivity {
    RecyclerView candidates;
    Button vote;
    String name,password,key,aadhar;
    ArrayList<Candidate> candidateslist = new ArrayList<>();
    RequestQueue queue;
    int selction=0;
    SharedPreferences sharedPreferences;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_candidate_list);
        candidates = findViewById(R.id.candidateslist);
        loadlist(-1);
        vote = findViewById(R.id.vote);
        vote.setVisibility(View.GONE);
        candidateslist.add(new Candidate(R.drawable.girl, "A", "SAAP"));
        candidateslist.add(new Candidate(R.drawable.professor, "B", "DJP"));
        candidateslist.add(new Candidate(R.drawable.teacher, "C", "RONGRESS"));
        candidateslist.add(new Candidate(R.drawable.user, "D", "INDEPENDENT"));
        candidateslist.add(new Candidate(R.drawable.nota, "E", "NOTA"));
        queue= Volley.newRequestQueue(getApplicationContext());
        boolean forvoiting = getIntent().getBooleanExtra("voting", false);
        sharedPreferences=getSharedPreferences(getString(R.string.pref),MODE_PRIVATE);

        if (forvoiting) {
            name=getIntent().getStringExtra("name");
            password=getIntent().getStringExtra("password");
            aadhar=getIntent().getStringExtra("aadhar");
            key=getIntent().getStringExtra("key");
            vote.setVisibility(View.VISIBLE);
            candidates.addOnItemTouchListener(
                    new RecyclerItemClickListener(this, candidates, new RecyclerItemClickListener.OnItemClickListener() {
                        @Override
                        public void onItemClick(View view, int position) {
                            loadlist(position);
                        }

                        @Override
                        public void onLongItemClick(View view, int position) {

                        }
                    }));
        }


        vote.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                makingvote(sharedPreferences.getString(getString(R.string.block2),""));

            }
        });


    }

    private void makingvote(String BASE_URL) {
        Toast.makeText(CandidateList.this,""+BASE_URL,Toast.LENGTH_SHORT).show();
        if(BASE_URL.equals("")) {
            Toast.makeText(CandidateList.this,"Please check links in settings",Toast.LENGTH_SHORT).show();
            return;
        }


        StringRequest makevote = new StringRequest(Request.Method.POST, BASE_URL + "/cast_vote", new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
                Log.d("TAG", "onResponse: "+response);
            if(response.equals("1")){
                Toast.makeText(CandidateList.this,"Vote Casted successfully",Toast.LENGTH_LONG).show();
                finish();
            }else {
                Toast.makeText(CandidateList.this,"Error in casting votes \n" +
                        "Please check your details",Toast.LENGTH_LONG).show();
            }

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
                params.put("name", name);
                params.put("key", key);
                params.put("password", password);
                params.put("aadhar_id",aadhar);
                params.put("candidate_id",(1000001+selction)+"");
                return params;
            }
        };

        queue.add(makevote);

    }

    private void loadlist(int selction) {
        this.selction=selction;
        candidates.setLayoutManager(new LinearLayoutManager(this));
        candidates.setAdapter(new candidatesadapter(this, candidateslist, selction));
        candidates.scrollToPosition(selction);
    }
}
