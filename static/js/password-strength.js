/**
 * password_strength_plugin.js
 * Copyright (c) 20010 myPocket technologies (www.mypocket-technologies.com)


 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:

 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.

 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 * @author Darren Mason (djmason9@gmail.com)
 * @date 3/13/2009
 *
 * @author Dean Rzonca (drzonca@evernote.com)
 * @date 6/28/2012
 *
 * @projectDescription Password Strength Meter is a jQuery plug-in provide you smart algorithm to detect a password strength. Based on Firas Kassem orginal plugin - http://phiras.wordpress.com/2007/04/08/password-strength-meter-a-jquery-plugin/
 * @version 1.0.1
 *
 * @requires jquery.js (tested with 1.3.2)
 * @param shortPass:	"shortPass",	//optional
 * @param badPass:		"badPass",		//optional
 * @param validPass:	"validPass",	//optional
 * @param strongPass:	"strongPass",	//optional
 * @param baseStyle:	"testResult",	//optional
 * @param msgStyle:		"passMsg",		//optional
 *
*/

(function($){
	$.fn.resultStyle = "";

	 $.fn.passStrength = function(options) {

		 var defaults = {
				noPass:         "noPass",
				noPassMsg:		"",
				shortPass: 		"shortPass",
				shortPassMsg:	"",
				invalidPass:    "invalidPass",
				invalidPassMsg: "",
				badPass:		"badPass",
				badPassMsg:		"",
				validPass:		"validPass",
				validPassMsg:	"",
				strongPass:		"strongPass",
				strongPassMsg:	"",
				baseStyle:		"testResult",
				msgStyle:		"passMsg",
				validPattern:     ""
			};
		 	var opts = $.extend(defaults, options);

		 	var validRegex = new RegExp(opts.validPattern);

		 	return this.each(function() {
		 		 var obj = $(this);



		 		$(obj).unbind(".pass").bind("keyup.pass blur.pass", function(event)
		 		{
					// Let's not tell the user the password is too short if they're still typing
		 			var field = $(this);
		 			if (event.type == "blur") {
		 				setTimeout(function() {$.fn.update(field, true);}, 500);  // Add a slight delay on blur, so other controls don't move when the user clicks them
		 			} else {
		 				$.fn.update(field, false);
		 			}

		 		});

		 		//FUNCTIONS
		 		$.fn.update = function(field,checkLength) {
		 			var password = field.val();
		 			var results = $.fn.teststrength(password,opts,checkLength);

					$.fn.clearStyles(field);
					field.addClass(opts.baseStyle).addClass(field.resultStyle);

					field.nextAll("." + opts.msgStyle).remove();
          field.after("<div class=\""+opts.msgStyle+" "+field.resultStyle+"\"></div>");
          field.next("." + opts.msgStyle).text(results);
          if (window.parent && window.parent.registrationFeedbackCallback) {
            window.parent.registrationFeedbackCallback(field, true);
          } else if (window.registrationFeedbackCallback) {
            window.registrationFeedbackCallback(field, true);
          }
		 		};

		 		$.fn.teststrength = function(password,option,checkLength){

		 			 	this.resultStyle = option.noPass;

		 			 	if (password.length == 0) {
		 			 		return option.noPassMsg;
		 			 	}

		 			 	if (password.length < 6) {
		 			 		if (checkLength) {
		 			 			this.resultStyle = option.shortPass;
		 			 			return option.shortPassMsg;
		 			 		}
		 			 		return "";
		 			 	}

		 			 	// The regex we provide by default checks for length as
		 			 	// well as valid characters, but we want to show a separate
		 			 	// error for length, so we do that first
		 			 	if (!validRegex.test(password)) {
		 			 		this.resultStyle = option.invalidPass;
		 			 		return option.invalidPassMsg;
		 			 	}

		 			 	// The original plugin had more complex rules, but we're
		 			 	// simplifying them for now

              //password is too short, just numbers or just chars
		 			    if (password.length < 8 || password.match(/^([a-z]|[A-Z])+$/) || password.match(/^([0-9])+$/)) {
		 			    	this.resultStyle = option.badPass;
		 			    	return option.badPassMsg;
		 			    }

		 			    //password has at least one symbol, lowercase letter, uppercase letter and number
		 			    if (password.match(/([!,@,#,$,%,^,&,*,?,_,~])/) && password.match(/([a-z])/)
		 			        && password.match(/([A-Z])/) && password.match(/([0-9])/)) {
		 			    	this.resultStyle = option.strongPass;
		 			    	return option.strongPassMsg;
		 			    }

		 			    //password has letters and numbers, but no symbols
		 			    this.resultStyle = option.validPass;
		 			    return option.validPassMsg;
		 		};

		 		$.fn.clearStyles = function(field) {
		 			field.removeClass(opts.baseStyle).removeClass(opts.noPass).removeClass(opts.shortPass).removeClass(opts.badPass).removeClass(opts.validPass).removeClass(opts.strongPass);
		 		};

		 		$.fn.clearStyles($(this));

		 		$(window).unload(function() {
		 		  $.fn.clearStyles($(this));
		 		});
		  });
	 };
})(jQuery);


$.fn.checkRepetition = function(pLen,str) {
 	var res = "";
     for (var i=0; i<str.length ; i++ )
     {
         var repeated=true;

         for (var j=0;j < pLen && (j+i+pLen) < str.length;j++){
             repeated=repeated && (str.charAt(j+i)==str.charAt(j+i+pLen));
             }
         if (j<pLen){repeated=false;}
         if (repeated) {
             i+=pLen-1;
             repeated=false;
         }
         else {
             res+=str.charAt(i);
         }
     }
     return res;
	};