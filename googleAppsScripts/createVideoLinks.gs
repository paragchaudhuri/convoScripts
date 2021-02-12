function linkVideos() {
  
  //1. ID of spreadsheet where video links have to be added
  var spreadsheetId = 'ADD-THE-ID-OF-THE-SPREADSHEET-THAT-WILL-CONTAIN-THE-VIDEO LINKS';
  var ss = SpreadsheetApp.openById(spreadsheetId);
  SpreadsheetApp.setActiveSpreadsheet(ss)


  //2. NAME of the sheet in which the video links have to be added
  var sheet = ss.getSheetByName('ADD-THE-NAME-OF-THE-SHEET-THAT-WILL-CONTAIN-THE-VIDEO-LINKS');
  
  //3. Set the row numbers for the cells where the links need to be copied (omit the header - i.e., row 1)
  var startRow = _SET_THIS_;
  var endRow = _SET_THIS_;


  //4. VERIFY THAT data is columns A to K in the sheet named above (Column A will become column number 0 below in the for loop). If not modify cellRange accordingly. 
  var cellRange = 'A'+startRow+':K'+endRow;
  var degreeMovieCellRange = 'K'+startRow+':K'+endRow;
  
  var range = sheet.getRange(cellRange);
  var values = range.getValues();
 
  var degreeMovieLinks = new Array(endRow-startRow+1);
  for (var i = 0; i < degreeMovieLinks.length; i++) {
    degreeMovieLinks[i] = new Array(1);
  }
  
  function setUrlFromId(id) { return "https://drive.google.com/uc?export=download&id="+id; }
  
  //5. This is the ID of the folder where the video files are uploaded   
  var degreeMovieAssetFolder=DriveApp.getFolderById('SET-THE-ID-OF-ViDEO-SOURCE-FOLDER'); 
    
  var degreeMovieAllFilesIterator=degreeMovieAssetFolder.getFiles();
  
  //6. Change 180 to number of rows in the sheet
  var degreeMovieFileListName= new Array(180);
  var degreeMovieFileListId= new Array(180);
  
  var fileCount=0
  var degreeMovieFile;
  while(degreeMovieAllFilesIterator.hasNext()) {
    degreeMovieFile=degreeMovieAllFilesIterator.next();
    degreeMovieFileListName[fileCount]=degreeMovieFile.getName().toLowerCase();
    degreeMovieFileListId[fileCount]=degreeMovieFile.getId();
    fileCount++;
  }

  //This is for debugging - check this and see it matches number of uploaded files
  Logger.log("Degree Movie Files Found: "+fileCount);
     
  
  for (var row = 0; row < values.length; row++) {

    //7. This line assumer that the ROLL NUMBERS are in column 6 of the sheet. If not modify accordingly.  
    var rollno = values[row][6].toString().toLowerCase();
    var degreefilename=rollno+".mp4";
    
    var degreeMovieFileUrl="";
    var degreeNameIndex=degreeMovieFileListName.indexOf(degreefilename);
    if (degreeNameIndex != -1) {
      var fileId=degreeMovieFileListId[degreeNameIndex];
      degreeMovieFileUrl = setUrlFromId(fileId);
    }
    
    degreeMovieLinks[row]=[degreeMovieFileUrl];
  }
  
  sheet.getRange(degreeMovieCellRange).setValues(degreeMovieLinks)
}