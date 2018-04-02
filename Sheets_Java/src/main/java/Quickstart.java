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
            // Build a new authorized API client service.
            Sheets service = getSheetsService();

            /* set up data pull from google sheet ( QR Code Generator )
             * link : https://docs.google.com/spreadsheets/d/1S2yF4qEinMXgbFFOOI4g5e3s_O6msvr6PWOO8SOXdwk/edit#gid=0
             */
            String spreadsheetId = "1S2yF4qEinMXgbFFOOI4g5e3s_O6msvr6PWOO8SOXdwk";
            String range = "Sheet1!C2:G";

            ValueRange response = service.spreadsheets().values()
                .get(spreadsheetId, range)
                .execute();

            List<List<Object>> values = response.getValues();
          
            // file to write to
            File file = new File("/Users/jessietrieu/repos/PCW_APP_2018/Sheets_Java/data/Sheet1.txt");
            PrintWriter printWriter = null;
            
            try {
                // establish database connection and statements/prepared statements/results
                cnc = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/PCW_APP?serverTimezone=PST", "PCW", "Pcw2018!!!!!"); //?autoReconnect=true&useSSL=false
                PreparedStatement ps = null;
                PreparedStatement upd = null;
                ResultSet res1 = null;
                String st = "select id from auth_user where email = ?";
                String update = "update PCW_APP_profile set qr_code = ? where user_id = ?";

                printWriter = new PrintWriter(file);
                if (values == null || values.size() == 0) {
                   printWriter.println("No data found.");
                } else {
                   printWriter.print("Email, QR Code Link\n");
                    /* 
                       Print columns C and G, which correspond to indices 0 and 4.
                       Pull Initial Email and QR Code and insert into DB
                    */ 
                   for (List row : values) { 
                        printWriter.printf("%s, %s\n", row.get(0), row.get(4));
                        String email = row.get(0).toString();
                        String code = row.get(4).toString();
                        ps = cnc.prepareStatement(st);
                        ps.setString(1,email);
                        res1 = ps.executeQuery();
                        while( res1.next() ) {
                            upd = cnc.prepareStatement(update);
                            upd.setString(1, code);
                            int id = res1.getInt("id");
                            upd.setInt(2, id);
                            upd.executeUpdate(update);
                        }
                    }
                } 
            }
            catch (SQLException e) {
                e.printStackTrace();
            }
            catch (FileNotFoundException e){
                e.printStackTrace();
            }
            finally {
                if( printWriter != null ) {
                   printWriter.close();
                }
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

        try {
            // List of emails from rows ( checkins ) that fall between start and end dates 
            ArrayList<String> checkedRows = new ArrayList<String>();

            // Build a new authorized API client service.
            Sheets service = getSheetsService();

            /* set up data pull from google sheet ( PCW2018 Form )
             * link : https://docs.google.com/spreadsheets/d/1cgN8kAuWosIRPfvAduCtJCjZx8VECPeo241SlCsUvhk/edit#gid=570217724
             */
            String spreadsheetId = "1cgN8kAuWosIRPfvAduCtJCjZx8VECPeo241SlCsUvhk";
            String range = "Form Responses 1!A2:D";

            ValueRange response = service.spreadsheets().values()
                .get(spreadsheetId, range)
                .execute();
        
            List<List<Object>> values = response.getValues();

            // file to write to
            File file = new File("/Users/jessietrieu/repos/PCW_APP_2018/Sheets_Java/data/Sheet2.txt");
            PrintWriter printWriter = null;
            int i = 0;
            try {
                // establish database connection and statements/prepared statements/results
                cnc = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/PCW_APP?serverTimezone=PST", "PCW", "Pcw2018!!!!!"); //?autoReconnect=true&useSSL=false
                PreparedStatement ps = null;
                ResultSet res1 = null;
                ResultSet res2 = null;
                Statement stmt = null;
                Statement upd = null;
                String st = "select * from PCW_APP_signintime";
                String pst = "select * from PCW_APP_profile p, auth_user au where au.id = p.user_id and ? = au.email";
                String update = "update PCW_APP_profile set signed_in = 1";

                while(i < 2) {
                    printWriter = new PrintWriter(file);
                    if (values == null || values.size() == 0) {
                       printWriter.println("No data found.");
                    } else {
                       printWriter.print("Timestamp, QR Code Link\n");

                        /* 
                           Filter out pulled date to match start and end time
                           Print columns A and D, which correspond to indices 0 and 3. ( Timestamp & Email )
                        */
                       for (List row : values) { 
                          stmt = cnc.createStatement();
                          res1 = stmt.executeQuery(st);
                          while( res1.next() ) {
                            Timestamp start = res1.getTimestamp("startTime");
                            Timestamp end = res1.getTimestamp("endTime");
                            Timestamp dt = Timestamp.valueOf(row.get(0).toString());
                            if( dt.before(end) && dt.after(start) ) {
                                checkedRows.add(row.get(3).toString());
                                System.out.println("First filter");
                                printWriter.printf("%s, %s\n", row.get(0), row.get(3));
                            }
                          }
                       }

                       // filter 2: sets signedIn to 1
                       for(String row : checkedRows) {
                            String email = row;
                            ps = cnc.prepareStatement(pst);
                            ps.setString(1,email);
                            res2 = ps.executeQuery();
                            upd = cnc.createStatement();
                            while( res2.next() ) {
                                upd.executeUpdate(update);
                            }
                       }
                    }
                    // 2 second delay
                    Thread.sleep(2000);
                    System.out.println("Testing..." + new Date());
                    i++;
                }
            }
            catch (SQLException e) {
                e.printStackTrace();
            }
            catch (FileNotFoundException e){
                e.printStackTrace();
            }
            catch (InterruptedException e) {
                e.printStackTrace();
            }
            finally {
                if( printWriter != null ) {
                   printWriter.close();
                }
                closeEm(cnc);
            }
        }
        catch ( IOException e ) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) throws IOException {
        insertQR(); // runs once
        checkSignIn();
    }
}