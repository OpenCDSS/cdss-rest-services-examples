
    (function (TelemetryTimeSeriesRaw, undefined) {
        /**
         * @param {function} callback          Function whose first parameter contains the TelemetryTimeSeriesRaw data, or null if an error occurs
         * @param {pager}    pager             Object that holds paging info. Fields are "pageSize" and "pageIndex"
         * @param {string}   apiKey            Api key or token from Portal to allow users more requests and data rows per day
         * @param {string}   abbrev            string input. Add an asterisk on the front and/or end to be used as a wildcard. Station Abbreviation
         * @param {date}     endDate           Object or date input. Object must contain "min" and/or "max" field. End Date Time
         * @param {bool}     includeThirdParty Boolean input. Value must be "true" or "false". Include third party data?
         * @param {date}     modified          Object or date input. Object must contain "min" and/or "max" field. Date record last modified
         * @param {string}   parameter         string input. Add an asterisk on the front and/or end to be used as a wildcard. Measured parameter. Enter one or more, separated by commas (with or without spaces between)
         * @param {date}     startDate         Object or date input. Object must contain "min" and/or "max" field. Start Date Time
        **/
        TelemetryTimeSeriesRaw.getData = function(callback, pager, apiKey, abbrev, endDate, includeThirdParty, modified, parameter, startDate) {
            var query;
            var handleAsGeoJson;
            handleAsGeoJson = false;
            query = "format=jsonforced";
            pager = pager != null ? Object.assign(pager) : new pager(null, 1);
            var pagerQuery = processPager(pager);
            var hasARequiredGroup = abbrev != null;
            if (!hasARequiredGroup) {
                console.log("abbrev required");
                return;
            }
                query = addToQuery(query, processString("apiKey", apiKey));
            query = addToQuery(query, processString("abbrev", abbrev));
            query = addToQuery(query, processDate("endDate", endDate));
            query = addToQuery(query, processBool("includeThirdParty", includeThirdParty));
            query = addToQuery(query, processDate("modified", modified));
            query = addToQuery(query, processString("parameter", parameter));
            query = addToQuery(query, processDate("startDate", startDate));
            var getListObject = function (returnObject) {
                if (returnObject != null) {
                    if (handleAsGeoJson === true) {
                        if (returnObject.GeoJsonFeatureCollection != null)
                            return returnObject.GeoJsonFeatureCollection.features;
                    }
                    else {
                        return returnObject.ResultList;
                    }
                }
                return null;
            };
            var getListField = getListObject;
            var getListLength = function (returnObject) {
                var listField = getListObject(returnObject);
                return listField != null ? listField.length : 0;
            };
            var getPropertiesField = function (list, index) {
                var item = list[index];
                var propField = handleAsGeoJson === true ? item.properties : item;
                return propField;
            };
            var dateRegex = /^(\d{1,4}[-\/]){2}(\d{1,4})([T_ ](\d{1,2}:){0,2}(\d{1,2})(.\d+)?([-+]\d{1,2}(:\d{1,2})?)?)?$/;
            var setDates = function (obj) {
                for (var prop in obj) {
                    if (obj.hasOwnProperty(prop)) {
                        var content = obj[prop];
                        if (content == null) content = "";
                        if (dateRegex.test(content)) {
                            var date = Date.parse(content);
                            if (!isNaN(date)) {
                                date = new Date(date);
                                obj[prop] = date;
                            }
                        }
                    }
                }
            }
            var baseUrl = "https://dwr.state.co.us/Rest/GET/api/v2/telemetrystations/telemetrytimeseriesraw/";
            var prePagingQuery = query;
            var download = function (url, innerCallback, innerPager) {
                var nullUrl = url == null;
                var nullCallback = innerCallback == null;
                if (nullCallback || nullUrl) {
                    if (nullCallback) console.log("callback cannot be null");
                    if (nullUrl) console.log("Error creating url, please check parameters");
                    return;
                }
                url = encodeURI(url);
                var xhr = new XMLHttpRequest();
                xhr.open('GET', url);
                xhr.onload = function () {
                    if (xhr.status === 200) {
                        var responseObject = JSON.parse(xhr.responseText);
                        setDates(responseObject);
                        //console.log("success");
                        //console.log(responseObject);
                        var resultList = getListObject(responseObject);
                        if (resultList.length > 0) {
                            for (var i = 0; i < resultList.length; i++) {
                                var item = getPropertiesField(resultList, i);
                                setDates(item);
                            }
                        }
                        var returnObject = {
                            /**
                             * Calls the callback with data the next page if there is a next page, otherwise calls the callback with null
                             * @param {function} nextCallback Function whose first parameter contains the TelemetryTimeSeriesRaw data, or null if an error occurs
                             **/
                            next: function (nextCallback) {
                                var newPager = Object.assign(innerPager);
                                if (newPager.pageIndex == null) newPager.pageIndex = 1;
                                if (responseObject.PageCount > newPager.pageIndex) newPager.pageIndex++;
                                else {
                                    console.log("No more pages");
                                    if (nextCallback != null) nextCallback(null);
                                    return;
                                }
                                var nextPagerQuery = processPager(newPager);
                                var nextQuery = addToQuery(prePagingQuery, nextPagerQuery);
                                var nextUrl = addQueryToUrl(baseUrl, nextQuery);
                                download(nextUrl, nextCallback, newPager);
                            },
                            /**
                             * Calls the callback with data the previous page if there is a previous page, otherwise calls the callback with null
                             * @param {function} prevCallback Function whose first parameter contains the TelemetryTimeSeriesRaw data, or null if an error occurs
                             **/
                            prev: function (prevCallback) {
                                var newPager = Object.assign(innerPager);
                                if (newPager.pageIndex == null) newPager.pageIndex = 1;
                                if (1 < newPager.pageIndex) newPager.pageIndex--;
                                else {
                                    console.log("No more pages");
                                    if (prevCallback != null) prevCallback(null);
                                    return;
                                }
                                var prevPagerQuery = processPager(newPager);
                                var prevQuery = addToQuery(prePagingQuery, prevPagerQuery);
                                var prevUrl = addQueryToUrl(baseUrl, prevQuery);
                                download(prevUrl, prevCallback, newPager);
                            },
                            url: url,
                            getListObject: function () { return getListObject(responseObject); },
                            getListField: function () { return getListField(responseObject); },
                            getListLength: function () { return getListLength(responseObject); },
                            getPropertiesField: function (index) { return getPropertiesField(getListField(responseObject), index); },
                            responseObject: responseObject
                        };
                        innerCallback(returnObject);
                        return;
                    }
                    console.log("Request failed");
                    console.log(xhr.status);
                    console.log(xhr.responseText);
                    innerCallback(null);
                    return;
                };
                xhr.send();
                //console.log(url);
            }
            query = addToQuery(prePagingQuery, pagerQuery);
            //console.log(query);
            var finalUrl = addQueryToUrl(baseUrl, query);
            download(finalUrl, callback, pager);
        }
        TelemetryTimeSeriesRaw.createPager = function(pageSize, pageIndex) {
            return {
                pageSize: pageSize,
                pageIndex: pageIndex
            };
        }
        function addToQuery(query, toAdd) {
            if (query == null || toAdd == null || toAdd.length === 0) return query;
            if (query.length === 0) return toAdd;
            var lastChar = query.charAt(query.length - 1);
            if (lastChar !== "?" && lastChar !== "&") query += "&";
            return query += toAdd;
        }
        function addQueryToUrl(url, query) {
            if (url == null || query == null || url.length === 0) return null;
            if (query.length === 0) return url;
            var urlEndsWithQ = url.charAt(url.length - 1) === "?";
            var queryEndsWithQ = query.charAt(0) === "?";
            if (urlEndsWithQ && queryEndsWithQ) query = query.substring(1);
            if (!urlEndsWithQ && !queryEndsWithQ) url += "?";
            return url + query;
        }

        function processNumber(name, numberObj) {
            var query = "";
            if (numberObj == null) return query;
            if (numberObj !== "" && !isNaN(numberObj)) {
                query = addToQuery(query, name + "=" + numberObj);
            }
            return query;
        }
        function processDate(name, dateObj) {
            var query = "";
            if (dateObj == null) return query;
            var date;
            if (dateObj !== "" && isValidDate(dateObj)) {
                date = new Date(dateObj);
                query = addToQuery(query, name + "=" + formatDate(date));
            }
            return query;
        }

        function processString(name, stringObj) {
            var query = "";
            if (stringObj != null && stringObj.toString().length > 0) {
                query = addToQuery(query, name + "=" + stringObj.toString());
            }
            return query;
        }

        function processPager(pagerObj) {
            var query = "";
            if (pagerObj == null) return query;
            if (pagerObj.pageSize != null && pagerObj.pageSize !== "" && !isNaN(pagerObj.pageSize)) {
                query = addToQuery(query, "pageSize=" + pagerObj.pageSize);
            }
            if (pagerObj.pageIndex != null && pagerObj.pageIndex !== "" && !isNaN(pagerObj.pageIndex)) {
                query = addToQuery(query, "pageIndex=" + pagerObj.pageIndex);
            }
            return query;
        }
        function processBool(name, boolObj) {
            var query = "";
            if (boolObj == null) return query;
            if (boolObj === false || boolObj === true) boolObj = boolObj.toString().toLowerCase();
            if (boolObj === "false" || boolObj === "true") {
                query = addToQuery(query, name + "=" + boolObj);
            }
            return query;
        }

        function isValidDate(date) {
            return date && (
                (Object.prototype.toString.call(date) === "[object Date]" && !isNaN(date))
                ||
                (typeof date === "string" && /^(\d{1,2}\/){2}(\d{4})([T_](\d{1,2}:){0,2}(\d{1,2})(.\d+)?([-+]\d{1,2}(:\d{1,2})?)?)?$/.test(date))
            );
    }
    function formatDate(date) {
        var formatted = (date.getMonth() + 1).toString().padStart(2, "0") + "/" + date.getDate().toString().padStart(2, "0") + "/" + date.getYear().toString();
        var hour = date.getHour();
        var minute = date.getHour();
        if (hour != 0 || minute != 0) {
            formatted += "_" + hour.toString().padStart(2, "0") + ":" + minute.toString().padStart(2, "0");
        }
        return formatted;
    }
    }(window.TelemetryTimeSeriesRaw = window.TelemetryTimeSeriesRaw || {}));
