
/**
 * Подготавливает данные (перевод твоей prepare_company_data на JS).
 * 
 * @param {Array<Object>} companyData - сырой ответ API
 * @param {Array<Object>} companyIdsArray - полный массив кампаний для type
 * @return {Array<Array<*>>} - массив строк для таблицы (без заголовков)
 */
function prepareCompanyData(companyData, companyIdsArray) {
  const order = [
    "views", "clicks", "ctr", "cpc", "sum", "atbs", "orders", "cr", "shks", "sum_price", 
    "name", "nmId", "date", "advertId", "Тип компании", "canceled", "appType"
  ];

  const companyTypes = {
    4: 'кампания в каталоге (устаревший тип)',
    5: 'кампания в карточке товара (устаревший тип)',
    6: 'кампания в поиске (устаревший тип)',
    7: 'кампания в рекомендациях на главной странице (устаревший тип)',
    8: 'автоматическая кампания',
    9: 'Аукцион'
  };

  const appTypes = {
    0: "неизвестно",
    1: "сайт",
    32: "Android",
    64: "IOS",
  };

  const result = [];

  companyData.forEach(row => {
    const advertId = row.advertId || null;

    (row.days || []).forEach(dayData => {
      const date = dayData.date || '';

      (dayData.apps || []).forEach(appData => {
        const rowData = {};

        order.forEach(columnName => {
          if (appData.hasOwnProperty(columnName)) {
            if (columnName === "appType") {
              rowData[columnName] = appTypes[appData[columnName]] || appTypes[0];
            } else {
              rowData[columnName] = appData[columnName];
            }
          } else if (['name', 'nmId'].includes(columnName)) {
            const nms = appData.nms || [];
            rowData[columnName] = nms.length > 0 ? nms[0][columnName] : '';
          } else if (columnName === "date") {
            rowData[columnName] = date;
          } else if (columnName === "advertId") {
            rowData[columnName] = advertId;
          } else if (columnName === 'Тип компании') {
            const matchingCompany = companyIdsArray.find(c => c.advertId === advertId);
            rowData[columnName] = matchingCompany ? companyTypes[matchingCompany.type] || 'Неизвестно' : 'Неизвестно';
          } else {
            rowData[columnName] = '';  // По умолчанию пусто, если не найдено
            Logger.log(`Неизвестная колонка: ${columnName}`);
          }
        });

        // Преобразуем в массив по order
        const rowArray = order.map(col => rowData[col] || '');
        result.push(rowArray);
      });
    });
  });

  return result;
}

/**
 * Пишет подготовленные данные в лист, начиная с указанной строки.
 * Возвращает новый rowIndex после записи.
 * 
 * @param {Array<Array<*>>} preparedData - массив строк
 * @param {string} sheetName
 * @param {number} startRowIndex - с какой строки начинать (обычно 2+)
 * @return {number} новый startRowIndex
 */
function writeTableToSheet222(preparedData, sheetName, startRowIndex = 2) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
  if (!sheet) {
    throw new Error(`Лист '${sheetName}' не найден`);
  }

  if (preparedData.length === 0) {
    return startRowIndex;
  }

  const numRows = preparedData.length;
  const numCols = preparedData[0].length;

  sheet.getRange(startRowIndex, 1, numRows, numCols).setValues(preparedData);

  // Флаш, чтобы пользователь видел прогресс (опционально)
  SpreadsheetApp.flush();

  return startRowIndex + numRows;
}

function makeReklama2() {
  const option_sheet = SpreadsheetApp.getActive().getSheetByName('Настройки');
  const TOKEN = option_sheet.getRange('B1').getValue(); 
  Logger.log(TOKEN)
  if (true){
    var companyIds = getCompanyIds(TOKEN);
    Utilities.sleep(60 * 1000); 
  }
  else {
    var companyIds = [{'advertId': 18756437, 'changeTime': '2025-10-26T23:19:19.112103+03:00', 'type': 9, 'status': 11}, {'advertId': 20024932, 'changeTime': '2025-11-03T19:18:37.959039+03:00', 'type': 9, 'status': 11}, {'advertId': 20521925, 'changeTime': '2025-10-26T23:39:37.924513+03:00', 'type': 9, 'status': 11}, {'advertId': 21187826, 'changeTime': '2026-01-13T23:31:39.024123+03:00', 'type': 9, 'status': 11}, {'advertId': 21322492, 'changeTime': '2025-10-26T23:41:33.31204+03:00', 'type': 9, 'status': 11}, {'advertId': 21322578, 'changeTime': '2025-10-26T23:30:06.891333+03:00', 'type': 9, 'status': 11}, {'advertId': 21442644, 'changeTime': '2025-10-26T23:47:45.908938+03:00', 'type': 9, 'status': 11}, {'advertId': 23412760, 'changeTime': '2025-10-26T23:46:08.310827+03:00', 'type': 9, 'status': 11}, {'advertId': 23440008, 'changeTime': '2025-11-29T23:07:26.8814+03:00', 'type': 9, 'status': 11}, {'advertId': 24687726, 'changeTime': '2025-10-26T23:43:57.660454+03:00', 'type': 9, 'status': 11}, {'advertId': 24969153, 'changeTime': '2025-10-26T23:33:38.377958+03:00', 'type': 9, 'status': 11}, {'advertId': 25131207, 'changeTime': '2025-10-26T23:31:30.0157+03:00', 'type': 9, 'status': 11}, {'advertId': 25131244, 'changeTime': '2025-10-26T23:50:05.710561+03:00', 'type': 9, 'status': 11}, {'advertId': 25254578, 'changeTime': '2025-10-26T23:13:22.542531+03:00', 'type': 9, 'status': 11}, {'advertId': 27209756, 'changeTime': '2025-10-26T23:25:56.275845+03:00', 'type': 9, 'status': 11}, {'advertId': 27209802, 'changeTime': '2026-01-29T14:02:30.482275+03:00', 'type': 9, 'status': 11}, {'advertId': 27267445, 'changeTime': '2025-10-26T23:51:27.485329+03:00', 'type': 9, 'status': 11}, {'advertId': 27418801, 'changeTime': '2026-01-26T17:07:56.196701+03:00', 'type': 9, 'status': 11}, {'advertId': 27691616, 'changeTime': '2026-01-29T12:22:23.529191+03:00', 'type': 9, 'status': 11}, {'advertId': 27694889, 'changeTime': '2025-10-27T00:04:16.776718+03:00', 'type': 9, 'status': 11}, {'advertId': 27870105, 'changeTime': '2025-12-15T12:54:03.965284+03:00', 'type': 9, 'status': 11}, {'advertId': 28979178, 'changeTime': '2025-10-26T23:38:06.242982+03:00', 'type': 9, 'status': 11}, {'advertId': 31717606, 'changeTime': '2026-01-14T11:28:32.043694+03:00', 'type': 9, 'status': 11}, {'advertId': 16202721, 'changeTime': '2024-06-15T13:09:51.811551+03:00', 'type': 8, 'status': 7}, {'advertId': 18033108, 'changeTime': '2024-07-27T14:16:29.301506+03:00', 'type': 8, 'status': 7}, {'advertId': 18286591, 'changeTime': '2024-06-28T09:33:52.727611+03:00', 'type': 8, 'status': 7}, {'advertId': 18286612, 'changeTime': '2024-08-13T18:51:16.892013+03:00', 'type': 8, 'status': 7}, {'advertId': 18848284, 'changeTime': '2024-08-11T15:04:47.897214+03:00', 'type': 8, 'status': 7}, {'advertId': 18755174, 'changeTime': '2025-12-26T16:57:58.038113+03:00', 'type': 8, 'status': 9}, {'advertId': 19199058, 'changeTime': '2026-01-28T13:28:28.570359+03:00', 'type': 8, 'status': 9}, {'advertId': 20023751, 'changeTime': '2025-11-26T13:13:05.602705+03:00', 'type': 8, 'status': 9}, {'advertId': 20024913, 'changeTime': '2025-11-26T15:05:48.199336+03:00', 'type': 8, 'status': 9}, {'advertId': 21187819, 'changeTime': '2025-11-11T05:28:17.019926+03:00', 'type': 8, 'status': 9}, {'advertId': 21322526, 'changeTime': '2025-11-12T00:02:25.083511+03:00', 'type': 8, 'status': 9}, {'advertId': 21322593, 'changeTime': '2025-11-26T14:19:54.932635+03:00', 'type': 8, 'status': 9}, {'advertId': 21442668, 'changeTime': '2026-01-26T17:36:52.851378+03:00', 'type': 8, 'status': 9}, {'advertId': 22874760, 'changeTime': '2026-01-27T00:40:44.427826+03:00', 'type': 8, 'status': 9}, {'advertId': 18730842, 'changeTime': '2026-01-29T16:09:38.019227+03:00', 'type': 9, 'status': 9}, {'advertId': 18849479, 'changeTime': '2026-01-29T16:09:41.261839+03:00', 'type': 9, 'status': 9}, {'advertId': 20024947, 'changeTime': '2026-01-29T16:04:23.348629+03:00', 'type': 9, 'status': 9}, {'advertId': 22874691, 'changeTime': '2026-01-29T16:09:30.727412+03:00', 'type': 9, 'status': 9}, {'advertId': 22874741, 'changeTime': '2026-01-29T16:09:26.965974+03:00', 'type': 9, 'status': 9}, {'advertId': 23412779, 'changeTime': '2026-01-29T16:04:09.132262+03:00', 'type': 9, 'status': 9}, {'advertId': 25372939, 'changeTime': '2025-10-27T00:24:16.700722+03:00', 'type': 9, 'status': 9}, {'advertId': 27231445, 'changeTime': '2025-12-21T20:33:55.797272+03:00', 'type': 9, 'status': 9}, {'advertId': 18796197, 'changeTime': '2025-12-21T01:01:28.444325+03:00', 'type': 8, 'status': 11}, {'advertId': 18796871, 'changeTime': '2025-11-24T18:43:35.873338+03:00', 'type': 8, 'status': 11}, {'advertId': 19618892, 'changeTime': '2025-09-11T07:10:51.731178+03:00', 'type': 8, 'status': 11}, {'advertId': 20024700, 'changeTime': '2025-09-11T07:10:51.734732+03:00', 'type': 8, 'status': 11}, {'advertId': 20024945, 'changeTime': '2025-09-18T21:30:35.96239+03:00', 'type': 8, 'status': 11}, {'advertId': 20024964, 'changeTime': '2025-09-30T23:38:33.551232+03:00', 'type': 8, 'status': 11}, {'advertId': 20521952, 'changeTime': '2025-09-11T07:10:51.77948+03:00', 'type': 8, 'status': 11}, {'advertId': 22874707, 'changeTime': '2025-11-12T18:10:48.669126+03:00', 'type': 8, 'status': 11}, {'advertId': 23412774, 'changeTime': '2025-07-03T21:18:08.803638+03:00', 'type': 8, 'status': 11}, {'advertId': 23412787, 'changeTime': '2026-01-29T08:33:23.550121+03:00', 'type': 8, 'status': 11}, {'advertId': 23439998, 'changeTime': '2025-09-30T23:38:24.80154+03:00', 'type': 8, 'status': 11}, {'advertId': 24687750, 'changeTime': '2025-04-20T01:03:00.495759+03:00', 'type': 8, 'status': 11}, {'advertId': 27245807, 'changeTime': '2025-12-14T15:52:04.164549+03:00', 'type': 8, 'status': 11}, {'advertId': 27261820, 'changeTime': '2025-09-11T07:11:53.484134+03:00', 'type': 8, 'status': 11}, {'advertId': 27267422, 'changeTime': '2025-09-11T10:12:08.724126+03:00', 'type': 8, 'status': 11}, {'advertId': 27418823, 'changeTime': '2025-09-19T16:24:48.796034+03:00', 'type': 8, 'status': 11}, {'advertId': 18725752, 'changeTime': '2025-08-21T11:20:07.460434+03:00', 'type': 9, 'status': 7}, {'advertId': 18725788, 'changeTime': '2025-08-21T11:20:07.365534+03:00', 'type': 9, 'status': 7}, {'advertId': 18725864, 'changeTime': '2025-08-21T11:20:07.272526+03:00', 'type': 9, 'status': 7}, {'advertId': 18734302, 'changeTime': '2025-08-21T11:20:07.875065+03:00', 'type': 9, 'status': 7}, {'advertId': 18848694, 'changeTime': '2025-08-21T11:20:12.260139+03:00', 'type': 9, 'status': 7}, {'advertId': 20024678, 'changeTime': '2025-08-21T11:20:55.46166+03:00', 'type': 9, 'status': 7}, {'advertId': 20024900, 'changeTime': '2025-08-21T11:20:55.462492+03:00', 'type': 9, 'status': 7}, {'advertId': 20025050, 'changeTime': '2025-08-21T11:20:55.859796+03:00', 'type': 9, 'status': 7}, {'advertId': 20025055, 'changeTime': '2025-08-21T11:20:55.460116+03:00', 'type': 9, 'status': 7}, {'advertId': 20047110, 'changeTime': '2025-08-21T11:20:56.361452+03:00', 'type': 9, 'status': 7}]
  }
  var startDate = new Date(option_sheet.getRange("B3").getValue());
  var endDate = new Date(option_sheet.getRange("B4").getValue());
  fetchAndWriteRaklamaData(companyIds, startDate, endDate, 'Реклама');
}