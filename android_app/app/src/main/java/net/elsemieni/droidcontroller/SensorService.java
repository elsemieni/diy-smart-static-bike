package net.elsemieni.droidcontroller;

import android.app.IntentService;
import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Intent;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.os.IBinder;
import android.os.PowerManager;
import android.support.annotation.Nullable;
import android.util.Log;
import android.widget.Toast;
import com.github.nkzawa.socketio.client.IO;
import com.github.nkzawa.socketio.client.Socket;

import java.net.URISyntaxException;

public class SensorService extends NonStopIntentService implements SensorEventListener {

    private SensorManager mSensorManager;
    private PowerManager.WakeLock wakeLock;

    private Socket mSocket;
    private String socketAdress;

    public SensorService(String name) {
        super(name);
    }

    public SensorService() {
        super("");
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        Bundle extras = intent.getExtras();
        String address = (String) extras.get("address");
        {
            try {
                Log.d("BikeAndroid", "Starting socket client at: " + address);
                mSocket = IO.socket(address);
            } catch (URISyntaxException e) {
                Log.d("BikeAndroid", "Socket Error: " + e);
            }
        }
        mSocket.connect();

        Toast.makeText(this, "service starting", Toast.LENGTH_SHORT).show();
        return super.onStartCommand(intent,flags,startId);
    }

    public void onCreate() {
        Toast.makeText(this, "service creating", Toast.LENGTH_SHORT).show();
        super.onCreate();

        // initialize your android device sensor capabilities
        mSensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);

        // for the system's orientation sensor registered listeners
        mSensorManager.registerListener(this, mSensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE), SensorManager.SENSOR_DELAY_GAME);
        //mSensorManager.registerListener(this, mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER), SensorManager.SENSOR_DELAY_GAME);

        PowerManager powerManager = (PowerManager) getSystemService(POWER_SERVICE);
        wakeLock = powerManager.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK,
                "MyApp::MyWakelockTag");
        wakeLock.acquire();

    }

    //cuando llegan comunicaciones, llegan por aqui
    @Override
    protected void onHandleIntent(@Nullable Intent intent) {
        // Normally we would do some work here, like download a file.
        // For our sample, we just sleep for 5 seconds.
    }

    //se llama cuando se destruye el servicio
    public void onDestroy() {
        wakeLock.release();
        mSensorManager.unregisterListener(this);
        mSocket.disconnect();
        stopForeground(true);
        Toast.makeText(this, "service done", Toast.LENGTH_SHORT).show();
        super.onDestroy();
    }

    @Override
    public void onSensorChanged(SensorEvent sensorEvent) {
        //float degree = Math.round(sensorEvent.values[0]);
        if (mSocket != null) {
            String message = "[" + sensorEvent.values[0] + "," + sensorEvent.values[1]+"," +  sensorEvent.values[2] + "]";
            Log.d("BikeAndroid", "Sending: " + message);
            mSocket.emit("onCoords", message );
        } else {
            Log.d("BikeAndroid", "No socket");
        }

    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int i) {
        //nah, no lo usaremos
    }
}
