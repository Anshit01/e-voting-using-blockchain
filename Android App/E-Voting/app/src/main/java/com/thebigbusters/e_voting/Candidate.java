package com.thebigbusters.e_voting;


public class Candidate {
    private int image;
    private String name;
    private String party;

    public Candidate(int image, String name, String party) {
        this.image = image;
        this.name = name;
        this.party = party;
    }

    public int getImage() {
        return image;
    }

    public String getName() {
        return name;
    }

    public String getParty() {
        return party;
    }
}
