
/*
 * Copyright (C) 2010-2011 VTT Technical Research Centre of Finland.
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation;
 * version 2.1 of the License.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 */

/*
 * 
 */

package fi.vtt.noen.mfw.bundle.server.plugins.webui.sacservice;

import javax.xml.namespace.QName;
import javax.xml.ws.Service;
import javax.xml.ws.WebEndpoint;
import javax.xml.ws.WebServiceClient;
import javax.xml.ws.WebServiceFeature;
import java.net.MalformedURLException;
import java.net.URL;

/**
 * This class was generated by Apache CXF 2.3.0
 * Tue Jan 25 14:14:10 EET 2011
 * Generated source version: 2.3.0
 * 
 */


@WebServiceClient(name = "MFW_SAC_service", 
                  wsdlLocation = "file:MFW_SAC_EADS_proposal_v3.1.wsdl",
                  targetNamespace = "http://www.bugyobeyond.org/MFW_SAC/") 
public class MFWSACService extends Service {

    public final static URL WSDL_LOCATION;
    public final static QName SERVICE = new QName("http://www.bugyobeyond.org/MFW_SAC/", "MFW_SAC_service");
    public final static QName MFWSAC = new QName("http://www.bugyobeyond.org/MFW_SAC/", "MFW_SAC");
    static {
        URL url = null;
        try {
            url = new URL("file:MFW_SAC_EADS_proposal_v3.1.wsdl");
        } catch (MalformedURLException e) {
            System.err.println("Can not initialize the default wsdl from file:MFW_SAC_EADS_proposal_v3.1.wsdl");
            // e.printStackTrace();
        }
        WSDL_LOCATION = url;
    }

    public MFWSACService(URL wsdlLocation) {
        super(wsdlLocation, SERVICE);
    }

    public MFWSACService(URL wsdlLocation, QName serviceName) {
        super(wsdlLocation, serviceName);
    }

    public MFWSACService() {
        super(WSDL_LOCATION, SERVICE);
    }
    

    /**
     * 
     * @return
     *     returns MFWSAC
     */
    @WebEndpoint(name = "MFW_SAC")
    public MFWSAC getMFWSAC() {
        return super.getPort(MFWSAC, MFWSAC.class);
    }

    /**
     * 
     * @param features
     *     A list of {@link javax.xml.ws.WebServiceFeature} to configure on the proxy.  Supported features not in the <code>features</code> parameter will have their default values.
     * @return
     *     returns MFWSAC
     */
    @WebEndpoint(name = "MFW_SAC")
    public MFWSAC getMFWSAC(WebServiceFeature... features) {
        return super.getPort(MFWSAC, MFWSAC.class, features);
    }

}
