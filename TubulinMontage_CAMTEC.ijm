@ String (label = "File suffix", value = ".czi") suffix

//This Macro works only with .czi files from the CAMTEC confocal.
//It can handle either single slices or z-stacks, and make multi-slice or single-slice montages.

in_dir = getDirectory("Choose a Directory")
processFolder(in_dir);


function processFolder(in_dir) {
	print(in_dir);
	list = getFileList(in_dir);
	list = Array.sort(list);
	cont = 0;
	out_dir = in_dir + "Montage\\";
	
	for (i = 0; i < list.length; i++) {
		
		//if(File.isDirectory(in_dir + File.separator + list[i]))
			//processFolder(in_dir + File.separator + list[i]);
		if(endsWith(list[i], suffix)){
			cont = openImage(list[i], in_dir, out_dir);
			if(cont==0){
				i = list.length*2;
			}
		}
	}
	print("Done")
}


function openImage(file, in_dir, out_dir){
	print(file);
	path = in_dir + file;
	run("Bio-Formats Importer", "open=[" + path + "] autoscale color_mode=Composite split_focal view=Hyperstack stack_order=XYCZT");
	print("Processing: " + path );

	Dialog.create("Skip Image?");
	Dialog.addRadioButtonGroup("Skip?", newArray("Yes", "No"), 1, 2, "No");
	Dialog.show();
	
	choice = Dialog.getRadioButton();
	if(choice == "Yes"){
		close("*");
		return 1;
	}

	
	sliceList = getList("image.titles");
	n = sliceList.length;
	print(n);

	if (n==1) {
		imgProcess(sliceList[0]);
		makeMontageSingle(file, sliceList[0], "", in_dir, out_dir);
	} else {
		labels = newArray(n);
		defaults = newArray(n);
		Array.fill(defaults, false);
		for (j=0; j<n; j++){
			labels[j] = "Z = "+j;
		}

		options = newArray("Multi-slice", "Single Slices", "Both");

		
		Dialog.create("Choose slices");
		
		Dialog.addRadioButtonGroup("Montage Type", options, 2, 1, options[1]);

		Dialog.addCheckboxGroup(n, 1, labels, defaults);
		Dialog.show();

		option_choice = Dialog.getRadioButton();
		slices = newArray(n);
		for (j=0; j<n; j++){
			slices[j] = Dialog.getCheckbox();
			if (!slices[j]){
				close(sliceList[j]);
			}
		}

		//Set brightness values for all slices
		run("Concatenate...", "all_open title="+file+" keep open");
		imgVals = imgProcess(file);
		
		if (option_choice == "Single Slices"){
			selectWindow(file);
			close();
			for (j=0; j<n; j++){
				if (slices[j]) {
					imgSet(sliceList[j], imgVals);
					makeMontageSingle(file, sliceList[j], j, in_dir, out_dir);	
				}
			run("Close All")
			}
		} else if (option_choice == "Multi-slice"){
			makeMontageMulti(file, in_dir, out_dir);
			run("Close All")
		} else if (option_choice == "Both") {
			makeMontageMulti(file, in_dir, out_dir);
			for (j=0; j<n; j++){
				if (slices[j]) {
					imgSet(sliceList[j], imgVals);
					makeMontageSingle(file, sliceList[j], j, in_dir, out_dir);	
				}
			}
			run("Close All")
			
		}
		
	}

	Dialog.create("Next Image?");
	Dialog.addRadioButtonGroup("Open Next?", newArray("Yes", "No"), 1, 2, "Yes");
	Dialog.show();
	
	choice = Dialog.getRadioButton();
	if(choice == "Yes"){
		return 1;
	}
	if(choice == "No"){
		return 0;
	}

}


function imgProcess(window){
	
	selectImage(window);
	run("Brightness/Contrast...");
	Stack.setChannel(2);
	run("Enhance Contrast", "saturated=0.15");
	Stack.setChannel(1);
	setMinAndMax(100, 200);	
	waitForUser("Brightness \n For nanoparticles: Adjust min to remove background, then set max. \n Brightness values will be carried to all images.");
	
	Stack.setChannel(1);
	getMinAndMax(min1, max1);
	Stack.setChannel(2);
	getMinAndMax(min2, max2);
	
	

	makeRectangle(0, 0, 100, 100);
	waitForUser("Crop");
	getSelectionBounds(x, y, width, height);
	run("Crop");
	imgVals = newArray(min1, max1, min2, max2, x, y, width, height);
	return imgVals;
	
}

function imgSet(window, imgVals){
	selectImage(window);
	run("Brightness/Contrast...");
	Stack.setChannel(2);
	setMinAndMax(imgVals[0], imgVals[1]);
	Stack.setChannel(1);
	setMinAndMax(imgVals[2], imgVals[3]);

	makeRectangle(imgVals[4], imgVals[5], imgVals[6], imgVals[7]);
	run("Crop");
}


function makeMontageSingle(file, window, z, in_dir, out_dir){
	selectImage(window);
	run("Arrange Channels...", "new=21");
	run("Stack to RGB", "keep");
	selectImage(window);
	run("Stack to Images");
	run("Images to Stack", "name=Stack title=[] use");
	Stack.setChannel(1);
	run("Scale Bar...", "width=25 height="+floor(4*getHeight()/1024)+" font=14 color=White background=None location=[Lower Right] bold hide");
	run("Reverse");
	run("Make Montage...", "rows=1 columns="+nSlices+" scale=1 border=2");

	outfile = substring(file, 0, indexOf(file,'.'))+"_"+z+"_montage.bmp";
	saveAs("BMP", out_dir+outfile);
	selectImage("Stack");
	close();
	selectImage(outfile);
	close();
	return;
	
}

function makeMontageMulti(file, in_dir, out_dir){
	
	run("Stack to RGB", "frames");
	window = getTitle();
	run("Scale Bar...", "width=25 height="+floor(4*getHeight()/1024)+" font=14 color=White background=None location=[Lower Right] bold hide label");
	run("Make Montage...", "rows=2 columns="+floor((nSlices+1)/2)+" scale=1 border=2");
	outfile = substring(file, 0, indexOf(file,'.'))+"_Zmontage.bmp";
	saveAs("BMP", out_dir+outfile);
	selectImage(window);
	close();
	selectImage(outfile);
	close();
	return;
	
}