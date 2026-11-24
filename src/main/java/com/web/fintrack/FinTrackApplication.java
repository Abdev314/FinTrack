package com.web.fintrack;

import com.web.fintrack.api.IllegalArgumentExceptionMapper;
import com.web.fintrack.api.RecordResource;

import javax.ws.rs.core.Application;
import java.util.HashSet;
import java.util.Set;
import com.web.fintrack.config.CorsFilter;

public class FinTrackApplication extends Application {

    @Override
    public Set<Class<?>> getClasses() {
        Set<Class<?>> classes = new HashSet<>();
        classes.add(RecordResource.class);
        classes.add(IllegalArgumentExceptionMapper.class);
        classes.add(CorsFilter.class);
        return classes;
    }
}