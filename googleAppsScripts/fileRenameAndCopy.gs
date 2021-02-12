function renameAndCopyFileByUrl() {
  //This works assuming we are renaming only one uploaded photo per roll number (that is the front face photo)

  //Don't use the Form Response sheet directly - use something that holds a copy of the Form Responses

  //1. Spreadsheet with renamed Student Data
  var spreadsheetId = 'ADD-THE-ID-OF-THE-SPREADSHEET-THAT-WILL-CONTAIN-THE-RENAMED-STUDENT-DATA';
  var ss = SpreadsheetApp.openById(spreadsheetId);
  SpreadsheetApp.setActiveSpreadsheet(ss);
  

  //2. The spreadsheet must have a copy of the original form responses in a sheet called "Original"
  var sheet = ss.getSheetByName('Original');

  //3. Create a sheet called "Renamed" - here we will put the urls to renamed files
  var renameSheet = ss.getSheetByName('Renamed');
  
  //Get a specific range - omitting the header. 
  //Remember the header is row 1

  //4. SET START ROW
  var startRow = _SET_THIS_;  
  //5. SET END ROW
  var endRow = _SET_THIS_;

  //6. VERIFY THAT data is columns A to L in the original sheet (Column A will become column number 0 below in the for loop). If not modify cellRange accordingly. 
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
  //7. Add the ID for the folder that will contain the renamed files - Note this is the DESTINATION folder
  var frontDataFolder = DriveApp.getFolderById('SET-THE-ID-OF-DESTINATION-FOLDER');

  //8. This is the column number in the "Original" sheet that has the url of the original file - SET THIS 
  var frontUrlColumn = _SET_THIS_;
  
  //These are helper functions
  function getIdFromUrl(url) { return url.match(/[-\w]{25,}$/); }
  function setUrlFromId(id) { return "https://drive.google.com/open?id="+id; }
  
  if (!values) {
    Logger.log('No data found.');
  } else {
    for (var row = 0; row < values.length; row++) {
      if (values[row][0] !== "") {
            
        //9. Change the column number to whichever column the ROLL NUMBER is stored in
        //Column numbers start from 0 here
        var rollnumber=values[row][_SET_THIS_];
        
        var filename_front=rollnumber+"_front.jpg";
        
        var urlFront = values[row][frontUrlColumn];
        var idFront = getIdFromUrl(urlFront);

        //This is only for debugging and can be commented out
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


