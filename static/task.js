
/**********************
* Domain general code *
**********************/

// Helper functions

function IsNumeric(input)
{
	return (input - 0) == input && input.length > 0;
}


// Assert functions stolen from 
// http://aymanh.com/9-javascript-tips-you-may-not-know#assertion
function AssertException(message) { this.message = message; }
AssertException.prototype.toString = function () {
	return 'AssertException: ' + this.message;
};

function assert(exp, message) {
	if (!exp) {
	  throw new AssertException(message);
	}
}

function insert_hidden_into_form(findex, name, value ) {
	var form = document.forms[findex];
	var hiddenField = document.createElement('input');
	hiddenField.setAttribute('type', 'hidden');
	hiddenField.setAttribute('name', name);
	hiddenField.setAttribute('value', value );
	form.appendChild( hiddenField );
}


// Preload images (not currently in use)
function imagepreload(src) 
{
	var heavyImage = new Image(); 
	heavyImage.src = src;
}

/** 
 * SUBSTITUTE PLACEHOLDERS WITH string values 
 * @param {String} str The string containing the placeholders 
 * @param {Array} arr The array of values to substitute 
 * From Fotiman on this forum:
 * http://www.webmasterworld.com/javascript/3484761.htm
 */ 
function substitute(str, arr) { 
	var i, pattern, re, n = arr.length; 
	for (i = 0; i < n; i++) { 
		pattern = "\\{" + i + "\\}"; 
		re = new RegExp(pattern, "g"); 
		str = str.replace(re, arr[i]); 
	} 
	return str; 
} 

function randrange ( lower, upperbound ) {
	// Finds a random integer from 'lower' to 'upperbound-1'
	return Math.floor( Math.random() * upperbound + lower );
}

// We want to be able to alias the order of stimuli to a single number which
// can be stored and which can easily replicate a given stimulus order.
function changeorder( arr, ordernum ) {
	var thisorder = ordernum;
	var shufflelocations = new Array();
	for (var i=0; i<arr.length; i++) {
		shufflelocations.push(i);
	}
	for (i=arr.length-1; i>=0; --i) {
		var loci = shufflelocations[i];
		var locj = shufflelocations[thisorder%(i+1)];
		thisorder = Math.floor(thisorder/(i+1));
		var tempi = arr[loci];
		var tempj = arr[locj];
		arr[loci] = tempj;
		arr[locj] = tempi;
	}
	return arr;
}

// Fisher-Yates shuffle algorithm.
// modified from http://sedition.com/perl/javascript-fy.html
function shuffle( arr, exceptions ) {
	var i;
	exceptions = exceptions || [];
	var shufflelocations = new Array();
	for (i=0; i<arr.length; i++) {
		if (exceptions.indexOf(i)==-1) { shufflelocations.push(i); }
	}
	for (i=shufflelocations.length-1; i>=0; --i) {
		var loci = shufflelocations[i];
		var locj = shufflelocations[randrange(0, i+1)];
		var tempi = arr[loci];
		var tempj = arr[locj];
		arr[loci] = tempj;
		arr[locj] = tempi;
	}
	return arr;
}

// This function swaps two array members at random, provided they are not in
// the exceptions list.
function swap( arr, exceptions ) {
	var i;
	var except = exceptions ? exceptions : [];
	var shufflelocations = new Array();
    for (i=0; i<arr.length; i++) {
        if (except.indexOf(i)==-1) { shufflelocations.push(i); }
    }
    
    for (i=shufflelocations.length-1; i>=0; --i) {
        var loci = shufflelocations[i];
        var locj = shufflelocations[randrange(0,i+1)];
        var tempi = arr[loci];
        var tempj = arr[locj];
    	arr[loci] = tempj;
    	arr[locj] = tempi;
    }
    
	return arr;
}


// Mean of booleans (true==1; false==0)
function boolpercent(arr) {
	var count = 0;
	for (var i=0; i<arr.length; i++) {
		if (arr[i]) { count++; } 
	}
	return 100* count / arr.length;
}

// View functions
function appendtobody( tag, id, contents ) {
	var el = document.createElement( tag );
	el.id = id;
	el.innerHTML = contents;
	return el;
}

function displayscreen( screenname ) {
    $("body").html( pages[screenname] );
}

// Gets a path string describing a line in Raphael.
function raphael_line( x1, y1, x2, y2 ) {
	pathstring = Raphael.format( "M{0},{1}L{2},{3}", x1, y1, x2, y2 );
	return pathstring;
}

function draw_tv(paper, length, angle, channel) {
	if (! isNaN(length)) {
		// TV params
		var angle_radiens = (angle / 180) * Math.PI,
			xdelta = length * Math.cos( angle_radiens ),
			ydelta = length * Math.sin( angle_radiens );
		
		// Attributes
		var strokewidth = 3,
			antenna_attr = {"stroke-width": strokewidth},
			stem_attr = {"stroke-width": strokewidth,
						 "stroke": "#999"};
		
		var stem = paper.
			path(raphael_line(stemx, stemy1, stemx, stemy2)).
			attr(stem_attr);
		
		var antenna = paper.
			path(raphael_line(stemx-xdelta, stemy2-ydelta,
							  stemx+xdelta, stemy2+ydelta)).
			attr(antenna_attr);
	}
	var tv = paper.image(tvImages[channel], tvx, tvy, tvwidth, tvheight);
}

// Form manipulation functions

//  Returns the form contents as a mapping.
function getFormFields () {
    var fields = {};
    
    var extractfun = function(i, val) { 
		var value;
		if (this.id !== this.value) value = this.value; 
		else value = this.checked;
		fields[this.id] = value; 
    };
    
	$('textarea').each( extractfun );
	$('select').each( extractfun );
	$('input').each( extractfun );
    
    return fields;
}

//  Writes the form ids and their responses to the datafile. 
function recordFormFields () {
    var fields = {};
    
    var extractfun = function(i, val) { 
		var value;
		if (this.id !== this.value) value = this.value; 
		else value = this.checked;
		datastring = datastring.concat( "\n", this.id, ":",  value);
    };
    
	$('textarea').each( extractfun );
	$('select').each( extractfun );
	$('input').each( extractfun );
	
	datastring = datastring.concat("\n");

    return fields;
}


// Data submission
// NOTE: Ended up not using this.
function posterror() { alert( "There was an error. TODO: Prompt to resubmit here." ); }
function submitdata() {
	$.ajax("submit", {
			type: "POST",
			async: false,
			data: {datastring: datastring},
			// dataType: 'text',
			success: thanks,
			error: posterror
	});
}


/********************
* TASK-GENERAL CODE *
********************/

// Globals defined initially.

// Stimulus info
var tvImages = {
	broken: "static/images/tvnan.png",
	ch1: "static/images/tv0.png",
	ch2: "static/images/tv1.png" 
};

// TV Stim variables
var maxantlength = 300, extrastem = 10,
    tvwidth=123, tvheight=100,
    tvcanvaswidth = Math.max( maxantlength, tvwidth ),
    tvcanvasheight = maxantlength + tvheight + extrastem,
    tvx=(tvwidth >= maxantlength ? 0 : (maxantlength-tvwidth)/2 ), tvy=tvcanvasheight - tvheight, 
    stemlength = (maxantlength / 2)+extrastem,
    stemx = tvx + (tvwidth/2), 
    stemy1 = tvy, stemy2 = tvy - stemlength;

// Timing variables
var prequerytime = 500; // Time after stim goes on, before query buttons go on.
var acknowledgmenttime = 500; // Time after response before stim goes off
var isi = 500; // ISI

// Task objects
var testobject;


// Mutable global variables
var responsedata = [],
    currenttrial = 1,
    datastring = "",
    lastperfect = false;

/********************
* Trial recording
********************/
function recordtesttrial(currentscreen, rt) {
	var trialvals = subjinfo + ',' + ["INSTRUCT", currentscreen, rt];
	datastring = datastring.concat( trialvals, "\n" );
}

/********************
* HTML snippets
********************/

var showpage = function(pagename) {
	$('body').html( pages[pagename] );
};

/**************************
* Experiment flow control *
**************************/

function nextblock() {
    if (blocks.length === 0) {
		givequestionnaire();
		return false;
	}
	currentBlock = blocks.shift();
	currentBlock.startblock();
	return true;
}

/********************
* Experiment block object
********************/
var currentBlock;

function ExperimentBlock() {
    this.count = 0;
}

// Mutable variables
ExperimentBlock.prototype.trialnum = 0;
ExperimentBlock.prototype.blocknum = 0;
ExperimentBlock.prototype.count = 0;
ExperimentBlock.prototype.total = 0;

// HTML snippets
ExperimentBlock.prototype.acknowledgment = '<p>Thanks for your response!</p>';
ExperimentBlock.prototype.buttonprompt = '<p id="prompt">Which channel do you think this TV picks up?  Try to be consistent.</p>';
ExperimentBlock.prototype.buttons = ExperimentBlock.prototype.buttonprompt + 
		'<div id="inputs">\
				<input type="button" id="ch1" value="CH1">\
				<input type="button" id="ch2" value="CH2">\
		</div>';
ExperimentBlock.prototype.continueprompt = '<p id="prompt">Please press continue to acknowledge.</p>';
ExperimentBlock.prototype.singlebutton = ExperimentBlock.prototype.continueprompt + 
		'<div id="inputs">\
				<input type="button" id="continue" value="Continue">\
		</div>';

// Draws a TV on the object's paper:
ExperimentBlock.prototype.draw_tv = function(length, angle, channel) {
    draw_tv( this.tvcanvas, length, angle, channel );
};

// Clears off the paper.
ExperimentBlock.prototype.clearTV = function() { this.tvcanvas.clear(); };

// Methods for doing a trial.
ExperimentBlock.prototype.addbuttons = function(resptype, callback) {
	resp_snippet = resptype === "choice" ? this.buttons : this.singlebutton;
	$('#query').html( resp_snippet );
	$('input').click( callback );
	$('#query').show();
};
ExperimentBlock.prototype.addprompt = function(buttons) {
	$('#query').html( (buttons ? this.buttonprompt : this.continueprompt) ).show();
};
ExperimentBlock.prototype.dotrial = function(stim) {
	var that = this;
	var length = stim[5],
	    angle = stim[6],
	    label = stim[7];
	this.draw_tv( length, angle, label );
	$("#countdown").html("TV #" + this.count + " / " + this.total);
	// this.addprompt();
	// stimon = new Date().getTime();
	setTimeout(
		function() {
			lock=false;
			var buttonson = new Date().getTime();
			that.addbuttons(
				stim[0],
				function() {
				var resp = this.value;
				var rt = (new Date().getTime()) - buttonson;
				that.recordtrial(stim, resp, rt);
				$('#query').html( that.acknowledgment );
				// Wait acknowledgmenttime to clear screen
				setTimeout(
					function() {
						$("#countdown").html("");
						$('#query').html('');
						that.clearTV();
						// Wait ISI to go to next trial.
						setTimeout( function(){that.nexttrial();}, isi );
					},
					acknowledgmenttime);
			});
		},
		prequerytime);
};

ExperimentBlock.prototype.recordtrial = function(stim, resp, rt) {
	trialvals = subjinfo + ',' + [this.trialnum, this.blocknum] + ',' + stim + ',' + [resp, rt];
	//console.log( trialvals );
	datastring = datastring.concat( trialvals, "\n" );
	currenttrial++;
};

ExperimentBlock.prototype.nexttrial = function() {
	if (this.items.length === 0) {
		this.finishblock();
	}
	else {
		ExperimentBlock.prototype.trialnum += 1;
		this.count += 1;
		var item = this.items.shift();
		this.dotrial( item );
	}
};

ExperimentBlock.prototype.startblock = function() { 
	this.nexttrial(); 
};
ExperimentBlock.prototype.finishblock = function() {
    nextblock();
};

/************************
* INSTRUCTIONS OBJECT   *
************************/
function InstructBlock(screens) {
	ExperimentBlock.call(this); // Call parent constructor
	this.items = screens;
}

InstructBlock.prototype = new ExperimentBlock();
InstructBlock.prototype.constructor = InstructBlock;

// Show an instruction screen.
InstructBlock.prototype.dotrial = function(currentscreen) {
	var that = this;
    // console.log(currentscreen);
	displayscreen( currentscreen );
	var timestamp = new Date().getTime();
	$('.continue').click( function() {
		that.recordtrial(currentscreen);
		that.nexttrial();
	});
	return true;
};

// Flow control:
InstructBlock.prototype.finishblock = function() {
    nextblock();
};

// Record
InstructBlock.prototype.recordtrial = function(currentscreen, rt) {
    recordtesttrial(currentscreen, rt);
};

/********************
* TRIAL OBJECT   *
********************/

// This object is for a block of trials where participants are shown a stimulus
// and queried about it.
function TrialBlock(stims) {
	ExperimentBlock.call(this); // Call parent constructor
	this.items = stims;
    this.total = stims.length;
}

TrialBlock.prototype = new ExperimentBlock();
TrialBlock.prototype.constructor = TrialBlock;

TrialBlock.prototype.startblock = function() { 
	TrialBlock.prototype.blocknum += 1;
    showpage( "test" );
	this.tvcanvas = Raphael(document.getElementById("stim"), tvcanvaswidth, tvcanvasheight );
	this.nexttrial(); 
};

// TrialBlock.prototype.finishblock = function() {
// 	nextblock(); // };

/************************
* PREQUIZ OBJECT   *
************************/

function PreQuiz() {
	this.items = {
		quiz: 'prequiz',
		success: 'presuccess',
		failure: 'prefail'
	};
}

PreQuiz.prototype = new InstructBlock();
PreQuiz.prototype.constructor = PreQuiz;

PreQuiz.prototype.validate = function(fields) {
    var missing = [];
    // Blocks to criterion
    if ( ! fields.knobs && 
         ! fields.length && 
         ! fields.screensize && 
         ! fields.angle ) missing.push("features");
    if ( ! IsNumeric(fields.numchannels) ) missing.push("numchannels");
    if ( ! fields.tuneyes && 
         ! fields.tuneno ) missing.push("alltuned");
    if ( ! fields.goalwatch &&
         ! fields.goaldesign &&
         ! fields.goalcat &&
         ! fields.goalfix ) missing.push("goal");
    if ( ! fields.brokenyes && 
         ! fields.brokenno ) missing.push("broken");
    return missing;
};

PreQuiz.prototype.checkform = function(fields) {
    var incorrect = [];
    // Question: What aspects of the TV are important?
    if (   fields.knobs || 
         ! fields.length || 
           fields.screensize || 
         ! fields.angle ) incorrect.push("features");
    // Question: how many channels are there?
    if ( fields.numchannels !== "2" ) incorrect.push("numchannels");
    // Question: Are all the TVs tuned to one of the channels?
    if ( ! fields.tuneyes || 
           fields.tuneno ) incorrect.push("alltuned");
   if ( fields.goalwatch ||
        fields.goaldesign ||
        !fields.goalcat ||
        fields.goalfix ) incorrect.push("goal");
    if ( ! fields.brokenyes || 
           fields.brokenno ) incorrect.push("broken");
    return incorrect;
};

// Show an instruction screen.
PreQuiz.prototype.dotrial = function(currentscreen) {
	var that = this;
    // console.log(currentscreen);
	displayscreen( this.items['quiz'] );
	var timestamp = new Date().getTime();
	$('.continue').click( function() {
        $(".warning").hide();
        var unvalidated = that.validate( getFormFields() );
		if ( unvalidated.length > 0 ) {
			$("#warntext").show();
			for (i=0; i<unvalidated.length; i++) {
				$("#" + unvalidated[i]).show();
			}
            // console.log( unvalidated );
			return false;
		}
		var rt = (new Date().getTime()) - timestamp;
		var fields = getFormFields();
		var passed = that.checkform( fields ).length === 0;
		that.recordtrial( "prequiz", (new Date().getTime())-timestamp, passed );
		recordFormFields();
		if ( passed ) {
			showpage(that.items['success']);
			startTask();
			$(".continue").click( function() { that.finishblock(); } );
		} else {
			showpage(that.items['failure']);
			$(".continue").click( function() {
				blocks = [ new InstructBlock( startinstructions.slice(0) ), new PreQuiz() ].concat(blocks);
				that.finishblock();
			});
		}
		return true;
	});
	return true;
};

// Flow control:
PreQuiz.prototype.startblock = function() { 
    this.dotrial();
};
PreQuiz.prototype.nexttrial = function() { };
PreQuiz.prototype.finishblock = function() {
    nextblock();
};

/*************
* Finish up  *
*************/
var givequestionnaire = function() {
	var timestamp = new Date().getTime();
	showpage('postquestionnaire');
	$("#continue").click(function () {
        recordtesttrial( "postquestionnaire", (new Date().getTime())-timestamp );
		cleanup();
		submitquestionnaire();
	});
	// $('#continue').click( function(){ trainobject = new TrainingPhase(); } );
	// postback();
};
var submitquestionnaire = function() {
	$('textarea').each( function(i, val) {
		datastring = datastring.concat( "\n", this.id, ":",  this.value);
	});
	$('select').each( function(i, val) {
		datastring = datastring.concat( "\n", this.id, ":",  this.value);
        });
	insert_hidden_into_form(0, "subjid", subjid );
	insert_hidden_into_form(0, "data", datastring );
	$('form').submit();
};

var startTask = function () {
	// Provide opt-out 
	window.onbeforeunload = function(){
    	$.ajax("quitter", {
    			type: "POST",
    			async: false,
    			data: {subjId: subjid, dataString: datastring}
    	});
		alert( "By leaving this page, you opt out of the experiment.  You are forfitting your $1.00 payment and your 1/10 chance to with $10. Please confirm that this is what you meant to do." );
		return "Are you sure you want to leave the experiment?";
	};
    $.ajax("inexp", {
            type: "POST",
            async: false,
            data: {subjId: subjid}
    });
};

var cleanup = function () {
	window.onbeforeunload = function(){ };
};

// vi: et! ts=4 sw=4
