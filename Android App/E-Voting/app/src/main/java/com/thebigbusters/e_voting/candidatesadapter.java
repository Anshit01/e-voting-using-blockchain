package com.thebigbusters.e_voting;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.RadioButton;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.cardview.widget.CardView;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;

public class candidatesadapter extends RecyclerView.Adapter<candidatesadapter.ViewHolder> {

    private Context context;
    private ArrayList<Candidate> candidateslist;
    private int selction;
    public candidatesadapter(Context context, ArrayList<Candidate> candidateslist,int selction) {
        this.context = context;
        this.candidateslist = candidateslist;
        this.selction=selction;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        LayoutInflater inflater=LayoutInflater.from(context);
        View v =inflater.inflate(R.layout.candiatesview,null);
        return new ViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        holder.image.setImageDrawable(context.getDrawable(candidateslist.get(position).getImage()));
        holder.name.setText(candidateslist.get(position).getName());
        holder.partyname.setText(candidateslist.get(position).getParty());
        if(selction==-1){
            holder.radioButton.setVisibility(View.GONE);

        }
        else if(position==selction){
            holder.radioButton.setChecked(true);
            holder.cardView.setCardBackgroundColor(context.getResources().getColor(R.color.blue_300));
        }
        else {
            holder.radioButton.setChecked(false);
            holder.cardView.setCardBackgroundColor(context.getResources().getColor(R.color.white));
        }
    }

    @Override
    public int getItemCount() {
        return candidateslist.size();
    }



    class ViewHolder extends RecyclerView.ViewHolder{
        TextView name,partyname;
        ImageView image;
        CardView cardView;
        RadioButton radioButton;
        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            name=itemView.findViewById(R.id.name);
            partyname=itemView.findViewById(R.id.party);
            image=itemView.findViewById(R.id.candidate_profile);
            cardView=itemView.findViewById(R.id.cardview);
            radioButton=itemView.findViewById(R.id.selction);
        }
    }
}
