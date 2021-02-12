function renameAndCopyFileByUrl() {
  //This works assuming we are renaming only one uploaded photo per roll number (that is the front face photo)

  //Don't use the Form Response sheet directly - use something that holds a copy of the Form Responses

  //Spreadsheet with renamed Student Data
  var spreadsheetId = 'ADD-THE-ID-OF-THE-SPREADSHEET-THAT-WILL-CONTAIN-THE-RENAMED-STUDENT-DATA';
  var ss = SpreadsheetApp.openById(spreadsheetId);
  SpreadsheetApp.setActiveSpreadsheet(ss);
  

  //The spreadsheet must have a copy of the original form responses in a sheet called "Original"
  var sheet = ss.getSheetByName('Original');

  //Create a sheet called "Renamed" - here we will put the urls to renamed files
  var renameSheet = ss.getSheetByName('Renamed');
  
  // Get a specific range - omitting the header. 
  // Remember the header is row 1

  //SET START ROW
  var startRow = _SET_THIS_;  
  //SET END ROW
  var endRow = _SET_THIS_;

  var cellRange = 'A'+startRow+':L'+endRow;

  //This is jsut for debugging if needed
  //Logger.log('Range: %s', cellRange);
  
  
  // Get all values - From first sheet
  var range = sheet.getRange(cellRange);
  var values = range.getValues();
  //Get a copy of the range of values
  var renamedValues = values.slice();
  
  var outputRange = renameSheet.getRange(cellRange);
  

  //Google Drive refers to files and folders by IDs
  //Add the ID for the folder that will contain the renamed files - Note this is the DESTINATION folder
  var frontDataFolder = DriveApp.getFolderById('SET-THE-ID-OF-DESTINATION-FOLDER');

  //This is the column number in the "Original" sheet that has the url of the original file  
  var frontUrlColumn = 10;
  
  //These are helper functions
  function getIdFromUrl(url) { return url.match(/[-\w]{25,}$/); }
  function setUrlFromId(id) { return "https://drive.google.com/open?id="+id; }
  
  if (!values) {
    Logger.log('No data found.');
  } else {
    for (var row = 0; row < values.length; row++) {
      // Print columns A and E, which correspond to indices 0 and 4.
      if (values[row][0] !== "") {
        
        //var timestamp=values[row][0];
        //var email=values[row][1];
        //var name=values[row][2];

        //Change the column number to whichever column the ROLL NUMBER is stored in
        var rollnumber=values[row][-FILL-ROLL-NUMBER-COLUMN-];
        
        var filename_front=rollnumber+"_front.jpg";
        
        var urlFront = values[row][frontUrlColumn];
        var idFront = getIdFromUrl(urlFront);
        
        Logger.log('Roll Number: %s, Url: %s, Id: %s', rollnumber, urlFront, idFront);
        
        var frontFile = DriveApp.getFileById(idFront);
        var newFrontFile = frontFile.makeCopy(filename_front, frontDataFolder);
        var newFrontFileUrl = setUrlFromId(newFrontFile.getId());
        renamedValues[row][frontUrlColumn] = newFrontFileUrl;
      }
    }
    outputRange.setValues(renamedValues);
  }
}


