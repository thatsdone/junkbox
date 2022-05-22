/**
 * SeleniumTest1
 * At the moment, almost just a copy from:
 *   https://applitools.com/blog/selenium-4-chrome-devtools/
 */
package com.github.thatsdone.junkbox;

import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.devtools.DevTools;
import java.util.HashMap;
import java.util.Map;
import java.lang.Thread;

public class SeleniumTest1 {

    final static String PROJECT_PATH = System.getProperty("user.dir");

    public static void main(String[] args){

	if (args.length >= 1) {
	    System.setProperty("webdriver.chrome.driver", PROJECT_PATH + args[0]);
	} else {
	    System.setProperty("webdriver.chrome.driver", PROJECT_PATH + "/src/main/resources/chromedriver");
	}
	    
        ChromeDriver driver;
        driver = new ChromeDriver();

        DevTools devTools = driver.getDevTools();
        devTools.createSession();
        Map deviceMetrics = new HashMap()
        {{
            put("width", 600);
            put("height", 1000);
            put("mobile", true);
            put("deviceScaleFactor", 50);
        }};
        driver.executeCdpCommand("Emulation.setDeviceMetricsOverride", deviceMetrics);
        driver.get("https://www.google.com");

	try {
	    Thread.sleep(3600 * 1000);
	} catch (Exception e){
	    e.printStackTrace();
	}
    }
}
