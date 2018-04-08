import com.google.api.client.auth.oauth2.Credential;
import com.google.api.client.extensions.java6.auth.oauth2.AuthorizationCodeInstalledApp;
import com.google.api.client.extensions.jetty.auth.oauth2.LocalServerReceiver;
import com.google.api.client.googleapis.auth.oauth2.GoogleAuthorizationCodeFlow;
import com.google.api.client.googleapis.auth.oauth2.GoogleClientSecrets;
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.http.HttpTransport;
import com.google.api.client.json.jackson2.JacksonFactory;
import com.google.api.client.json.JsonFactory;
import com.google.api.client.util.store.FileDataStoreFactory;
import com.google.api.services.sheets.v4.SheetsScopes;
import com.google.api.services.sheets.v4.model.*;
import com.google.api.services.sheets.v4.Sheets;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Connection;
import java.sql.Timestamp;
import java.io.*;
import java.util.*;
import java.util.Date;
import java.text.SimpleDateFormat;
import java.sql.ResultSetMetaData;

public class Quickstart {
    /** Application name. */
    private static final String APPLICATION_NAME =
        "Google Sheets API Java Quickstart";

    /** Directory to store user credentials for this application. */
    private static final java.io.File DATA_STORE_DIR = new java.io.File(
        System.getProperty("user.home"), ".credentials/sheets.googleapis.com-java-quickstart");

    /** Global instance of the {@link FileDataStoreFactory}. */
    private static FileDataStoreFactory DATA_STORE_FACTORY;

    /** Global instance of the JSON factory. */
    private static final JsonFactory JSON_FACTORY =
        JacksonFactory.getDefaultInstance();

    /** Global instance of the HTTP transport. */
    private static HttpTransport HTTP_TRANSPORT;

    /** Global instance of the scopes required by this quickstart.
     *
     * If modifying these scopes, delete your previously saved credentials
     * at ~/.credentials/sheets.googleapis.com-java-quickstart
     */
    private static final List<String> SCOPES =
        Arrays.asList(SheetsScopes.SPREADSHEETS, SheetsScopes.DRIVE);

    static {
        try {
            HTTP_TRANSPORT = GoogleNetHttpTransport.newTrustedTransport();
            DATA_STORE_FACTORY = new FileDataStoreFactory(DATA_STORE_DIR);
        } catch (Throwable t) {
            t.printStackTrace();
            System.exit(1);
        }
    }

    /**
     * Creates an authorized Credential object.
     * @return an authorized Credential object.
     * @throws IOException
     */
    public static Credential authorize() throws IOException {
        // Load client secrets.
        InputStream in =
            Quickstart.class.getResourceAsStream("/client_secret.json");
        GoogleClientSecrets clientSecrets =
            GoogleClientSecrets.load(JSON_FACTORY, new InputStreamReader(in));

        // Build flow and trigger user authorization request.
        GoogleAuthorizationCodeFlow flow =
                new GoogleAuthorizationCodeFlow.Builder(
                        HTTP_TRANSPORT, JSON_FACTORY, clientSecrets, SCOPES)
                .setDataStoreFactory(DATA_STORE_FACTORY)
                .setAccessType("offline")
                .build();
        Credential credential = new AuthorizationCodeInstalledApp(
            flow, new LocalServerReceiver()).authorize("user");
        System.out.println(
                "Credentials saved to " + DATA_STORE_DIR.getAbsolutePath());
        return credential;
    }

    /**
     * Build and return an authorized Sheets API client service.
     * @return an authorized Sheets API client service
     * @throws IOException
     */
    public static Sheets getSheetsService() throws IOException {
        Credential credential = authorize();
        return new Sheets.Builder(HTTP_TRANSPORT, JSON_FACTORY, credential)
                .setApplicationName(APPLICATION_NAME)
                .build();
    }

    // function to close connection
    public static void closeEm( Object... toClose ) {
        for( Object obj: toClose ) {
            if( obj != null )
                try {
                    obj.getClass().getMethod("close").invoke(obj);
                }
                catch ( Throwable t ) {
                    System.out.println("Log bad close");
                }
        }
    }

    public static void insertQR() {
        try {
            Class.forName("com.mysql.jdbc.Driver");
        } 
        catch ( ClassNotFoundException e) {
            e.printStackTrace();
        }
        Connection cnc = null;

        try {
            Sheets service = getSheetsService();

            /* set up data pull from google sheet ( QR Code Generator )
             * link : https://docs.google.com/spreadsheets/d/1_aJY0elhyylkqDlHWwDJbWQkrXzs5crQ-YXnvxT-97Y/edit#gid=0
             */
            String spreadsheetId = "1_aJY0elhyylkqDlHWwDJbWQkrXzs5crQ-YXnvxT-97Y";
            String range = "Sheet1!C2:G";

            ValueRange response = service.spreadsheets().values()
                .get(spreadsheetId, range)
                .execute();

            List<List<Object>> values = response.getValues();
            
            try {
                // establish database connection and statements/prepared statements/results
                cnc = DriverManager.getConnection("jdbc:mysql://wf-207-38-86-69.webfaction.com/pcw_app?serverTimezone=America/Los_Angeles", "pcw", "Pcw2018!!!!!"); //?autoReconnect=true&useSSL=false
                PreparedStatement ps = null;
                PreparedStatement upd = null;
                ResultSet res1 = null;
                String st = "select id from auth_user where email = ?";
                String update = "update PCW_APP_profile set QR_code = ?, Organization = ?, hostee = ? where user_id = ?"; //add hostee = ?

                /* 
                   Print columns C, D and G, which correspond to indices 0, 1 and 4.
                   Pull Initial Email and QR Code and insert into DB
                */ 
               for (List row : values) { 
                    String email = row.get(0).toString();
                    String org = row.get(1).toString();
                    String code = row.get(4).toString();
                    ps = cnc.prepareStatement(st);
                    ps.setString(1,email);
                    res1 = ps.executeQuery();
                    while( res1.next() ) {
                        upd = cnc.prepareStatement(update);
                        upd.setString(1, code);
                        upd.setString(2, org);
                        upd.setInt(3, 1);
                        int id = res1.getInt("id");
                        upd.setInt(4, id);
                        upd.executeUpdate();
                    }
                }
            } 
            catch (SQLException e) {
                e.printStackTrace();
            }
            finally {
                closeEm(cnc);
            }
        }
        catch ( IOException e ) {
            e.printStackTrace();
        }
    }

    public static void checkSignIn() {
        // setup for connection to database
        try {
            Class.forName("com.mysql.jdbc.Driver");
        } 
        catch ( ClassNotFoundException e) {
            e.printStackTrace();
        }

        Connection cnc = null;
        try{
            cnc = DriverManager.getConnection("jdbc:mysql://wf-207-38-86-69.webfaction.com/pcw_app?serverTimezone=America/Los_Angeles", "pcw", "Pcw2018!!!!!"); //?autoReconnect=true&useSSL=false
        }
        catch (SQLException e) {
            e.printStackTrace();
        }

        try {
            while (true) {
                ArrayList<String> checkedRows = new ArrayList<String>();
                Sheets service = getSheetsService();
                String spreadsheetId = "1L2fYLcD6bw5SS04khckeDATUPPqKRIJwOMEYrfQa1WU";
                String range = "Form Responses 1!A2:E";
                ValueRange response = service.spreadsheets().values().get(spreadsheetId, range).execute();
                List<List<Object>> values = response.getValues();

                try {
                    
                    PreparedStatement ps = null;
                    ResultSet res1 = null;
                    ResultSet res2 = null;
                    Statement stmt = null;
                    PreparedStatement upd = null;
                    String st = "select * from PCW_APP_signintime";
                    String pst = "select * from PCW_APP_profile p, auth_user au where au.id = p.user_id and ? = au.email";
                    String update = "update PCW_APP_profile set signed_in = 1 where user_id = ?";

                    /* 
                       Filter out pulled date to match start and end time
                       Print columns B and E, which correspond to indices 1 and 4. ( Formatted Timestamp & Email )
                    */
                    for (List row : values) { 
                        stmt = cnc.createStatement();
                        res1 = stmt.executeQuery(st);
                        while( res1.next() ) {
                            java.util.Calendar cal = Calendar.getInstance();
                            cal.setTimeZone(TimeZone.getTimeZone("PST"));
                            Calendar calendar = Calendar.getInstance();
                            calendar.setTime(new Date());
                            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
                            sdf.setTimeZone(TimeZone.getTimeZone("America/Los_Angeles"));
                            Timestamp start = Timestamp.valueOf(sdf.format(res1.getTimestamp("startTime")));
                            Timestamp end = Timestamp.valueOf(sdf.format(res1.getTimestamp("endTime")));
                            Timestamp dt = Timestamp.valueOf(row.get(1).toString());

                            if( dt.before(end) && dt.after(start) ) {
                                checkedRows.add(row.get(4).toString());
                            }
                        }
                    }

                    // filter 2: sets signedIn to 1
                    for(String row : checkedRows) {
                        String email = row;
                        ps = cnc.prepareStatement(pst);
                        ps.setString(1,email);
                        res2 = ps.executeQuery();
                        while( res2.next() ) {
                            int user = res2.getInt("user_id");
                            upd = cnc.prepareStatement(update);
                            upd.setInt(1, user);
                            upd.executeUpdate();
                        }
                    }
                }
                catch (SQLException e) {
                    e.printStackTrace();
                }
                Thread.sleep(2000); // 2 second delay
                System.out.println("Pulled..." + new Date());
            }
        }
        catch ( IOException e ) {
            e.printStackTrace();
        }
        catch (InterruptedException e) {
            e.printStackTrace();
        }
        finally {
            closeEm(cnc);
        }
    }

    public static void main(String[] args) throws IOException {
        insertQR(); // runs once
        checkSignIn();
    }
}