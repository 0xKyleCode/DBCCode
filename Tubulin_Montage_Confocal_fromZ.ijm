// Montages are saved into a folder named 'Montages' located in the same folder as the open image.
// You need to make the montages folder ahead of time, the macro doesn't create it.

// Start by opening an image or z-stack using Bio Formats Importer (should automatically run when opening a stack)
// If opening a z-stack, check the 'Split focal planes' box.
// This macro can only run on one slice at a time, so you'll have to open the stack again for each slice you want a montage of.




file = getTitle()
dir = getDirectory("image")
dir = dir + "Montage\\";

makeMontage(file, dir);

function makeMontage(file, dir){
	
	selectWindow(file);

	
	//run("Channels Tool...");
	run("Reverse");
	Stack.setDisplayMode("color");
	Stack.setChannel(1);
	run("Green");
	run("Enhance Contrast", "saturated=0.35");
	Stack.setChannel(2);
	run("Red");
	run("Enhance Contrast", "saturated=0.35");

	
	
	
	run("Make Composite", "display=Composite");
	

	run("Brightness/Contrast...");
	Stack.setChannel(1);
	run("Enhance Contrast", "saturated=0.35");
	Stack.setChannel(2);
	waitForUser("Set Brightness");

	makeRectangle(0, 0, 400, 400);
	waitForUser("Crop? Delete square to select full image");
	run("Crop");

	

	run("Stack to RGB");
	selectWindow(file);
	run("Stack to Images");
	run("Images to Stack", "name=Stack title=[] use");
	Stack.setChannel(1);
	run("Scale Bar...", "width=25 height=4 font=14 color=White background=None location=[Lower Right] bold hide");
	run("Reverse");
	run("Make Montage...", "columns=1 rows=3 scale=1 border=2");

	
	

	outfile = substring(file, 0, indexOf(file,'.'))+"_montage_slice.bmp";
	saveAs("BMP", dir+outfile);
	close("*");

	return 1;
}

function getItem(val){
	info = getImageInfo();

	if (val == "Size"){
		idx1 = indexOf(info, "history Acquisition Acquire.Scanner.XField.DisplayString");
		if (idx1==-1) return "";
		idx1 = indexOf(info, "=", idx1);
		if (idx1==-1) return "";
		idx2 = indexOf(info, " ", idx1+2);
		value = substring(info, idx1+2, idx2);
		print(val);
		print(value);
		return value;
	} else if(val == "Mag"){
		idx1 = indexOf(info, "history objective Magnification");
	} else if(val == "Gain1"){
		idx1 = indexOf(info, "history gain1");
	} else if(val == "Gain2"){
		idx1 = indexOf(info, "history gain1");
	} else if(val == "step1"){
		idx1 = indexOf(info, "history step1 Gain 2");
	} else if(val == "step2"){
		idx1 = indexOf(info, "history step2 Gain 1");
	} else if(val == "pix"){
		idx1 = indexOf(info, "SizeX");
	}
	
	if (idx1==-1) return "";
	idx1 = indexOf(info, "=", idx1);
	if (idx1==-1) return "";
	idx2 = indexOf(info, "\n", idx1+2);
	value = substring(info, idx1+2, idx2);
	print(val);
	print(value);
	return value;
}
