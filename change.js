static function OnBeforeResponse(oSession: Session) {
        if (m_Hide304s && oSession.responseCode == 304) {
            oSession["ui-hide"] = "true";
        }
        var isJson=oSession.ResponseHeaders.ExistsAndContains("Content-Type","json");

        if (oSession.fullUrl.Contains("skl.hdu.edu.cn")&&isJson) {

            oSession.utilDecodeResponse();
            
            oSession.SaveResponseBody("D:\\python_code\\I love Words\\questions.json");
          
		        }

    }
