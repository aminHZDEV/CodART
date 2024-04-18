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

package fi.vtt.noen.mfw.bundle.server.plugins.persistence;

import fi.vtt.noen.mfw.bundle.server.shared.datamodel.BMDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ServerEvent;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.TargetDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.Value;

import java.util.List;
import java.util.Map;

/**
 * @see PersistencePluginImpl for documentation of the methods.
 * @author Teemu Kanstren
 */
public interface PersistencePlugin {
  public List<ServerEvent> getEvents(int first, int count, ServerEvent.SortKey sortKey, boolean ascending);
  public int getEventCount();
  public List<Value> getValues(int first, int count, Value.SortKey sortKey, boolean ascending);
  public List<Value> getValues(long start, long end, Long[] bmids, Value.SortKey sort, boolean asc );
  public int getValueCount();
  public ProbeDescription createProbeDescription(Map<String, String> properties);
  public BMDescription createBMDescription(Map<String, String> properties);
  public TargetDescription createTargetDescription(Map<String, String> properties);
}
