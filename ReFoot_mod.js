/***********************************************************************/
/*                                                                     */
/*      ReFoot ::    Convert tagged text (back) to Footnotes           */
/*                                                                     */
/*      [Ver: 1.0b]    [Author: Marc Autret]    [Modif: 04/03/10]      */
/*      [Lang: EN]     [Req: InDesign CS4]      [Creat: 04/02/10]      */
/*                                                                     */
/*      Installation:                                                  */
/*                                                                     */
/*      1) Place the current file into Scripts/Scripts Panel/          */
/*                                                                     */
/*      2) Run InDesign, open a document, opt. select a text frame     */
/*                                                                     */
/*      3) Exec script from Window > Automatisation > Scripts          */
/*         (double-click on the script name)                           */
/*                                                                     */
/*      Bugs & Feedback : marc{at}indiscripts{dot}com                  */
/*                        www.indiscripts.com                          */
/*                                                                     */
/***********************************************************************/

var SCRIPT_NAME = "ReFoot 1.0b";

var FOOTNOTE_PATTERNS = {
	"[[NOTE]]note[[NOTE]]" : "\[\[NOTE]]((?:(?!\[\[NOTE]]).)*)\[\[NOTE]]",
	"<footnote>NOTE</footnote>" : "<footnote>([^<]+)</footnote>",
	"<note>NOTE</note>" : "<note>([^<]+)</note>",
	"<NOTE>" : "<([^>]+)>",
	};

/*var*/ comboBox = function(/*str*/msg, /*str[]*/items, /*str*/title)
//----------------------------
	{
	var ddList,
		gValid,
		w = new Window('dialog',' '+title),
		i, s;
		
	(w.add('statictext',undefined,msg,{multiline:true})).characters = msg.length;

	ddList = w.add('dropdownlist');
	for( i=0 ; i<items.length ; ++i )
		ddList.add((items[i] == '-') ? 'separator' : 'item', items[i]);
	
	gValid = w.add('group');
	w.defaultElement = gValid.add('button',undefined,"OK");
	w.cancelElement = gValid.add('button',undefined,"Cancel");

	ddList.selection = ddList.items[0];
	return  ( w.show() == 1 ) ?
		{index: (s=ddList.selection).index, item:s.text} :
		false;
	};

/*void*/ Application.prototype.main = function()
//----------------------------------------------------------
{
if ( this.documents.length <= 0 ) return;
var tg = this.selection[0] || this.activeDocument;
if( 'appliedFont' in tg ) tg = tg.parent;
if( tg.constructor == TextFrame ) tg = tg.parentStory;
if(! ('findGrep' in tg) ) return;

var fnPattern = (function()
	{
	var ptn, ptnItems=[], ret;
	for( ptn in FOOTNOTE_PATTERNS ) ptnItems.push(ptn);
	ret = comboBox("Select the footnote pattern used in the text:",
		ptnItems, SCRIPT_NAME);
	return ret && FOOTNOTE_PATTERNS[ret.item];
	})();

if( !fnPattern ) return;

var fnFinds = (function()
	{
	this.findGrepPreferences = this.changeGrepPreferences = null;
	this.findGrepPreferences.findWhat = fnPattern;
	var ret = tg.findGrep();
	this.findGrepPreferences = this.changeGrepPreferences = null;
	return ret;
	}).call(this);

var fnFind,
	fnText,
	rg = new RegExp(fnPattern),
	ip, fnParent, fn, count=0;

while( fnFind=fnFinds.pop() )
	{
	fnText = fnFind.contents.match(rg)[1];
	fnParent = fnFind.parent.getElements()[0];
	ip = fnFind.insertionPoints[0].index;
	try	{
		fnFind.remove();
		fn = fnParent.footnotes.add(LocationOptions.BEFORE, fnParent.insertionPoints[ip]);
		fn.texts[0].insertionPoints[-1].contents = fnText;
		++count;
		}
	catch(_){}
	}
	
alert((count)?
	(count+" footnote(s) successfully added."):
	"No footnote added. Make sure you use the relevant pattern."
	);
}

app.doScript('app.main();', ScriptLanguage.javascript,
undefined, UndoModes.entireScript, app.activeScript.displayName);