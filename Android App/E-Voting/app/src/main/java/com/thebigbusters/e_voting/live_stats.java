package com.thebigbusters.e_voting;

import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.anychart.AnyChart;
import com.anychart.AnyChartView;
import com.anychart.chart.common.dataentry.DataEntry;
import com.anychart.chart.common.dataentry.ValueDataEntry;
import com.anychart.chart.common.listener.Event;
import com.anychart.chart.common.listener.ListenersInterface;
import com.anychart.charts.Pie;
import com.anychart.enums.Align;
import com.anychart.enums.LegendLayout;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class live_stats extends AppCompatActivity {
    RequestQueue requestQueue;
    AnyChartView anyChartView;
    List<DataEntry> data = new ArrayList<>();
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_live_stats);
        requestQueue= Volley.newRequestQueue(this);
         anyChartView= findViewById(R.id.any_chart_view);
        anyChartView.setProgressBar(findViewById(R.id.progress_bar));
        makechart();
  //   getdata();
    }



    private  void  makechart(){
        Pie pie = AnyChart.pie();

        pie.setOnClickListener(new ListenersInterface.OnClickListener(new String[]{"x", "value"}) {
            @Override
            public void onClick(Event event) {
                Toast.makeText(live_stats.this, event.getData().get("x") + ":" + event.getData().get("value"), Toast.LENGTH_SHORT).show();
            }
        });

        data.add(new ValueDataEntry("SAAP", 6371664));
        data.add(new ValueDataEntry("RONGRESS", 789622));
        data.add(new ValueDataEntry("DJP", 7216301));
        data.add(new ValueDataEntry("INDEPENDENT", 1486621));
        data.add(new ValueDataEntry("NOTA", 1200000));

        pie.data(data);

        pie.title("Elections Results");

        pie.labels().position("outside");

        pie.legend().title().enabled(true);
        pie.legend().title()
                .text("Parties")
                .padding(0d, 0d, 10d, 0d);

        pie.legend()
                .position("center-bottom")
                .itemsLayout(LegendLayout.HORIZONTAL)
                .align(Align.CENTER);

        anyChartView.setChart(pie);

    }






    private void getdata(){
        String BASE_URL=getSharedPreferences(getString(R.string.pref),MODE_PRIVATE).getString(getString(R.string.block2),"");
        final StringRequest makevote = new StringRequest(Request.Method.GET, BASE_URL + "/get_result", new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
                Log.d("TAG", "onResponse: "+response);
                try {
                    JSONObject j=new JSONObject(response);
                    data.add(new ValueDataEntry("SAAP", (j.getInt("a"))));
                    data.add(new ValueDataEntry("DJP", (j.getInt("b"))));
                    data.add(new ValueDataEntry("RONGRESS", (j.getInt("c"))));
                    data.add(new ValueDataEntry("INDEPENDENT", (j.getInt("d"))));
                    data.add(new ValueDataEntry("NOTA", (j.getInt("e"))));
                    makechart();

                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {

            }
        }
        );

        requestQueue.add(makevote);


    }
}
