package com.peaktopper.playground;


import java.io.IOException;
import java.util.LinkedList;
import java.util.List;

import com.ECS.client.jax.*;

import org.jsoup.*;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class Playground {

	static final String ASSOCIATE_TAG = "test"; //WE NEED A WEBSITE AND TO SIGN UP AS AN AFFILIATE to get paid
	static final String ACCESS_KEY = "AKIAJF2ZX4IKRUJNEUQQ";
	
	AWSECommerceService service;
	AWSECommerceServicePortType port;
	
	public Playground() {
		// Set the service:
		service = new AWSECommerceService();
		service.setHandlerResolver(new AwsHandlerResolver("bL3I3m6q21q08yTvmnY9P2JgXa7rgSq4lt/zgNXY"));
		
		//Set the service port:
		port = service.getAWSECommerceServicePort();
	}
	
	
	public String findBrowseNode(String browseNodeId, String name, List<String> guides) {
		
		
				BrowseNodeLookupRequest browseNodeLookupRequest = new BrowseNodeLookupRequest();
				
				browseNodeLookupRequest.getBrowseNodeId().add(browseNodeId);
				
				BrowseNodeLookup browseNodeLookup = new BrowseNodeLookup();
				browseNodeLookup.setAssociateTag(ASSOCIATE_TAG);
				browseNodeLookup.setAWSAccessKeyId(ACCESS_KEY);
				browseNodeLookup.getRequest().add(browseNodeLookupRequest);
				
				BrowseNodeLookupResponse response = port.browseNodeLookup(browseNodeLookup);
				
				List<BrowseNode> browseNodes = response.getBrowseNodes().get(0).getBrowseNode().get(0).getChildren().getBrowseNode();		
				
				for(BrowseNode browseNode : browseNodes) {
					
					if(browseNode.getName().equals(name)) {
						return browseNode.getBrowseNodeId();
					} else if(browseNode.getName().contains(guides.get(0))) {
						String nextBrowseNode = browseNode.getBrowseNodeId();
						guides.remove(0);
						return findBrowseNode(nextBrowseNode, name, guides);
					}
				}
				return null;
	}
	
	public void itemSearch(String browseNodeId) {
		//Get the operation object:
		ItemSearchRequest itemRequest = new ItemSearchRequest();

		//Fill in the request object:
		itemRequest.setBrowseNode(browseNodeId);
		itemRequest.setSearchIndex("Electronics");
		itemRequest.getResponseGroup().add("ItemAttributes");
		itemRequest.getResponseGroup().add("Reviews");
		
		ItemSearch itemElement= new ItemSearch();
		itemElement.setAWSAccessKeyId(ACCESS_KEY);
		itemElement.getRequest().add(itemRequest);
		itemElement.setAssociateTag(ASSOCIATE_TAG);
		
		
		//Call the Web service operation and store the response
		//in the response object:
		ItemSearchResponse response = port.itemSearch(itemElement);
		
		List<Item> items = response.getItems().get(0).getItem();
		
		for(Item item: items) {
			String reviewUrl = item.getCustomerReviews().getIFrameURL();
			Document reviewDoc;
			try {
				reviewDoc = Jsoup.connect(reviewUrl).get();

				Elements histogramNums = reviewDoc.select(".crIFrameHeaderHistogram td[align=right]");
			
				for(Element e : histogramNums) {
				
				//	String num = Integer.parseInt(histogramNums);
				}
				
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			
		}
		
		
		  //Print Results to Screen
		  System.out.println(response.getItems().get(0).getItem().get(0).getDetailPageURL());
		
	}
	
	
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		//televisions - 493964
		
		LinkedList<String> guides = new LinkedList<String>();
		guides.add("Television");
		
		Playground pg = new Playground();
		
		String bn = pg.findBrowseNode("493964", "Televisions", guides);
		
		if(bn!=null) {
			pg.itemSearch(bn);
			
			
		}
	}
		
		
	

}
