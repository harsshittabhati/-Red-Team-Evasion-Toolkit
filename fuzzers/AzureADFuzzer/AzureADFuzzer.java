import com.azure.identity.ClientSecretCredential;
import com.azure.identity.ClientSecretCredentialBuilder;
import com.microsoft.graph.authentication.TokenCredentialAuthProvider;
import com.microsoft.graph.models.User;
import com.microsoft.graph.requests.GraphServiceClient;
import okhttp3.Request;

import java.util.Arrays;
import java.util.List;

public class AzureADFuzzer {
    public static void main(String[] args) {
        // Step 1: Define credentials
        final String clientId = "YOUR_CLIENT_ID";
        final String clientSecret = "YOUR_CLIENT_SECRET";
        final String tenantId = "YOUR_TENANT_ID";

        // Step 2: Authenticate
        ClientSecretCredential clientSecretCredential = new ClientSecretCredentialBuilder()
                .clientId(clientId)
                .clientSecret(clientSecret)
                .tenantId(tenantId)
                .build();

        List<String> scopes = Arrays.asList("https://graph.microsoft.com/.default");

        TokenCredentialAuthProvider authProvider = new TokenCredentialAuthProvider(scopes, clientSecretCredential);

        GraphServiceClient<Request> graphClient = GraphServiceClient
                .builder()
                .authenticationProvider(authProvider)
                .buildClient();

        // Step 3: Attempt enumeration
        try {
            System.out.println("== Azure AD Fuzzing Started ==");

            // Enumerate users
            List<User> users = graphClient.users().buildRequest().get().getCurrentPage();
            for (User user : users) {
                System.out.println("User: " + user.displayName + " | ID: " + user.id + " | Mail: " + user.mail);
            }

        } catch (Exception e) {
            System.out.println("Error during fuzzing: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
