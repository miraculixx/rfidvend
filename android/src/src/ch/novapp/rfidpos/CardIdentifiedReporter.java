package ch.novapp.rfidpos;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;

import android.os.AsyncTask;
import android.util.Log;

public class CardIdentifiedReporter extends AsyncTask<Object, Integer, String > {
	MainActivity callingActivity;
	
	//static String rfidpos_url = "http://localhost:5000";
	static String rfidpos_url = "http://novapp.eu01.aws.af.cm/";
	/**
	 * called upon execute of task
	 */
	@Override
	protected String doInBackground(Object... params) {
		try {
			callingActivity = (MainActivity)params[1];
			return reportCardIdentified((String)params[0]);
		} catch (IOException e) {
			e.printStackTrace();
			return "error";
		}
	}
	
	@Override
	protected void onPostExecute(String result) {
		super.onPostExecute(result);
		callingActivity.showResult(result);
	}
	
	/**
	 * Create a URL connection to report the card transaction
	 * @param cardid
	 * @return
	 * @throws IOException
	 */
	private String reportCardIdentified(String cardid) throws IOException {
		InputStream inputStream = null;
		String responseString = null;
		
		try {
			URL url = new URL(String.format("%s/cardtrx?cardid=%s", rfidpos_url, cardid));
			HttpURLConnection conn = (HttpURLConnection) url.openConnection();
			int response = conn.getResponseCode();
			Log.d(this.getClass().getSimpleName(), "The response is: "
					+ response);
			inputStream = conn.getInputStream();
			responseString = readResponseString(inputStream, 80);
		} finally {
			if (inputStream != null) {
				inputStream.close();
			}
		}
		
		return responseString;
	}

	/**
	 * Convert the input stream to a String object
	 * 
	 * @param stream
	 * @return
	 * @throws IOException
	 * @throws UnsupportedEncodingException
	 */
	private String readResponseString(InputStream stream, int len) throws IOException,
			UnsupportedEncodingException {
		Reader reader = new InputStreamReader(stream, "UTF-8");
		char[] buffer = new char[len];
		reader.read(buffer);
		return new String(buffer);
	}

}
