//@OnlyCurrentDoc
function onOpen(e) {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu("Import new order 👉️")
    .addItem("Import from Drive", "importCsvFromDrive")
    .addToUi();
}

function displayToastAlert(content) {
  SpreadsheetApp.getActive().toast(content, "⚠️ Alert");
}

function promptForUserInput(promptText) {
  var ui = SpreadsheetApp.getUi();
  var prompt = ui.prompt(promptText);
  return prompt.getResponseText();
}

function findFilesInDrive(fileName) {
  var files = DriveApp.getFilesByName(fileName);
  var result = [];
  while (files.hasNext()) {
    result.push(files.next());
  }
  return result;
}

function importCsvFromDrive() {
  var fileName = promptForUserInput(
    "Enter the URL of the CSV file to import from Google Drive"
  );
  var files = findFilesInDrive(fileName);
  if (files.length === 0) {
    displayToastAlert("No files found with name " + fileName);
  } else if (files.length > 1) {
    displayToastAlert(
      "Multiple files found with the name " +
        fileName +
        ". Please rename it as this program does not allow you to pick your file yet"
    );
  }

  var file = files[0];
  var contents = Utilities.parseCsv(file.getBlob().getDataAsString());
  writeCsvData(contents, fileName);
  displayToastAlert("File successfully uploaded");
}

function writeCsvData(data, fileName) {
  var ss = SpreadsheetApp.getActive();
  sheet = ss.insertSheet();
  sheet.getRange(1, 1, data.length, data[0].length).setValues(data);
  ss.getSheetByName(sheet.getName()).setName(fileName);
  // Add user columns:
  addUserColumn("Dany Boy", "F", data.length, sheet);
  addUserColumn("Paupo", "G", data.length, sheet);
  addUserColumn("Miss People G", "H", data.length, sheet);
  addUserColumn("La Cooooloc", "I", data.length, sheet);
  // Add quantity validation
  addValidation(data.length, "F", sheet);
  addValidation(data.length, "G", sheet);
  addValidation(data.length, "H", sheet);
  addValidation(data.length, "I", sheet);
  // Set the totals
  setTotal("F", data.length, sheet);
  setTotal("G", data.length, sheet);
  setTotal("H", data.length, sheet);
  setTotal("I", data.length, sheet);
  return sheet.getName();
}

function addUserColumn(userName, name, length, sheet) {
  var range = sheet.getRange(name + "1:" + name + String(length));
  var values = range.getValues();
  values[0][0] = userName;
  for (var i = i; i < values.length; i++) {
    values[i][0] = 0;
  }
  range.setValues(values);
}

function addValidation(length, column, sheet) {
  for (var i = 2; i <= length; i++) {
    var cell = sheet.getRange(column + String(i));
    cell.setValue(0);
    var quantity = parseInt(sheet.getRange("C" + String(i)).getValue());
    cell.setDataValidation(getQuantityRule(quantity, i));
  }
}

function getQuantityRule(quantity, index) {
  return SpreadsheetApp.newDataValidation()
    .requireValueInList([...Array(quantity + 1).keys()], true)
    .requireFormulaSatisfied(getFormula(index))
    .setHelpText("Number must be between 0 and " + String(quantity))
    .build();
}

function getFormula(index) {
  return (
    "=EQ(SUM(F" +
    String(index) +
    ",G" +
    String(index) +
    ",H" +
    String(index) +
    ", I" +
    String(index) +
    "), C" +
    String(index) +
    ")"
  );
}

function setTotal(column, length, sheet) {
  cell = sheet.getRange(column + String(length + 1));
  cell.setFormula(
    "=SUMPRODUCT(D2:D" +
      String(length) +
      "," +
      column +
      "2:" +
      column +
      String(length) +
      ")"
  );
}
